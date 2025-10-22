"""
KAB (Knowledge Base Article Builder) Manager

Manages KB article creation, searching, and linking following KCS standards.
Integrates with Red Hat Customer Portal Knowledge Base via Hydra REST API v2.

API Documentation:
- Base URL: https://access.redhat.com/hydra/rest/search/v2
- Search uses Apache Solr query syntax
- Authentication: Red Hat Customer Portal API Token (rh_jwt cookie)
- Requires Red Hat VPN for internal access
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import re
import os
import sys


class KABManager:
    """Manages Knowledge Base article operations via Hydra API v2."""

    def __init__(self, portal_token: Optional[str] = None):
        """
        Initialize KAB Manager with Red Hat Customer Portal authentication.
        
        Args:
            portal_token: Red Hat Customer Portal API token (JWT).
                         If not provided, attempts to load from environment.
        """
        self.kb_api_base = "https://access.redhat.com/hydra/rest/search/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Taminator/1.7.1 KABManager',
            'Accept': 'application/json'
        })
        
        # Set authentication token
        token = portal_token or os.getenv('RH_PORTAL_TOKEN')
        if token:
            # Hydra API uses JWT cookie for authentication
            self.session.cookies.set('rh_jwt', token, domain='access.redhat.com')
        
        # Note: Requires Red Hat VPN/Kerberos authentication and API token

    def search_kb_articles(self, query: str, product: Optional[str] = None, 
                          article_type: Optional[str] = None, limit: int = 20,
                          start: int = 0, sort: str = 'lastModifiedDate desc') -> Dict:
        """
        Search Knowledge Base articles using Hydra API v2.

        Args:
            query: Search keywords (Solr query syntax supported)
            product: Filter by product (e.g., "Red Hat Satellite", "Red Hat Enterprise Linux")
            article_type: Filter by documentKind ("Solution", "Article")
            limit: Maximum number of results (rows parameter)
            start: Offset for pagination
            sort: Sort order (e.g., "lastModifiedDate desc", "allTitle asc")

        Returns:
            Dictionary with:
                - numFound: Total results count
                - docs: List of KB article dictionaries
                - start: Current offset
                - rows: Results per page
                
        Example:
            kab = KABManager(portal_token="your_jwt_token")
            results = kab.search_kb_articles("ansible multipath", product="Red Hat Satellite")
            print(f"Found {results['numFound']} articles")
            for doc in results['docs']:
                print(f"{doc['id']}: {doc['title']}")
        """
        try:
            # Build Solr query parameters
            params = {
                'q': query if query else '*:*',  # Default to all if empty
                'rows': limit,
                'start': start,
                'sort': sort,
                'fl': 'id,allTitle,view_uri,lastModifiedDate,documentKind,product,abstract,kcsState'
            }

            # Build Solr filter query (fq) for precise filtering
            filters = []
            if product:
                # Exact product match with quotes for multi-word products
                filters.append(f'product:"{product}"')
            
            if article_type:
                # documentKind: Solution, Article, etc.
                filters.append(f'documentKind:"{article_type}"')
            
            if filters:
                params['fq'] = ' AND '.join(filters)

            # Call Hydra Search API v2 for KCS articles
            response = self.session.get(
                f"{self.kb_api_base}/kcs",
                params=params,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()
            response_data = data.get('response', {})
            
            # Parse results
            articles = []
            for item in response_data.get('docs', []):
                # Handle product field (can be array or string)
                products = item.get('product', [])
                if isinstance(products, list):
                    product_name = products[0] if products else 'Unknown'
                else:
                    product_name = products
                
                # Build full URL from view_uri
                view_uri = item.get('view_uri', '')
                if view_uri and not view_uri.startswith('http'):
                    full_url = f"https://access.redhat.com{view_uri}"
                else:
                    full_url = view_uri or f"https://access.redhat.com/solutions/{item.get('id', '')}"
                
                articles.append({
                    'id': item.get('id', ''),
                    'title': item.get('allTitle', 'Untitled'),
                    'product': product_name,
                    'type': item.get('documentKind', 'Article'),
                    'description': item.get('abstract', '')[:300],
                    'url': full_url,
                    'modified': item.get('lastModifiedDate', ''),
                    'kcs_state': item.get('kcsState', 'Unknown'),
                })

            return {
                'numFound': response_data.get('numFound', 0),
                'docs': articles,
                'start': response_data.get('start', 0),
                'rows': len(articles)
            }

        except requests.RequestException as e:
            print(f"Error searching KB articles: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text[:500]}", file=sys.stderr)
            print("Note: KB search requires Red Hat VPN and valid Portal API token", file=sys.stderr)
            return {'numFound': 0, 'docs': [], 'start': 0, 'rows': 0}

    def fetch_recent_kb_articles(self, author: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Fetch recent KB articles by author or recent activity.

        Args:
            author: Filter by author username
            limit: Maximum number of articles

        Returns:
            List of recent KB article dictionaries
        """
        try:
            params = {
                'rows': limit,
                'start': 0,
                'sort': 'lastModifiedDate desc'
            }

            if author:
                params['author'] = author

            response = self.session.get(
                f"{self.kb_api_base}/content/recent",
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            articles = []

            for item in data.get('items', []):
                articles.append({
                    'id': item.get('id', ''),
                    'title': item.get('title', 'Untitled'),
                    'product': item.get('product', 'Unknown'),
                    'status': item.get('status', 'Draft'),
                    'views': item.get('view_count', 0),
                    'lastModified': item.get('lastModifiedDate', '')[:10],  # Just date
                })

            return articles

        except requests.RequestException as e:
            print(f"Error fetching recent KB articles: {e}")
            return []

    def create_kb_article(self, article_data: Dict) -> Optional[Dict]:
        """
        Create a new KB article following KCS standards.

        Args:
            article_data: Dictionary containing:
                - title: Article title
                - product: Product name
                - type: Article type (solution, article, troubleshooting, how-to)
                - environment: Environment details
                - issue: Problem description
                - resolution: Solution steps
                - rootCause: (Optional) Root cause explanation
                - links: (Optional) Related links

        Returns:
            Dictionary with article_id, url, status, or None on error
        """
        try:
            # Format article according to KCS Content Standard 2.0
            kcs_formatted = self._format_kcs_article(article_data)

            # Submit to Customer Portal KB API
            response = self.session.post(
                f"{self.kb_api_base}/content",
                json=kcs_formatted,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()

            return {
                'article_id': result.get('id', ''),
                'url': result.get('view_uri', ''),
                'status': 'Draft',  # New articles start as drafts
                'message': 'KB article created successfully. Submitted for peer review.'
            }

        except requests.RequestException as e:
            print(f"Error creating KB article: {e}")
            return None

    def _format_kcs_article(self, article_data: Dict) -> Dict:
        """
        Format article data according to KCS Content Standard 2.0.

        The KCS standard requires:
        - Clear, customer-focused title
        - Environment section
        - Issue/Problem statement
        - Resolution with steps
        - Root Cause (optional)
        - Related links
        """
        formatted = {
            'title': article_data.get('title', ''),
            'product': article_data.get('product', ''),
            'documentKind': article_data.get('type', 'solution'),
            'content': {
                'environment': article_data.get('environment', ''),
                'issue': article_data.get('issue', ''),
                'resolution': article_data.get('resolution', ''),
            }
        }

        # Add optional fields
        if article_data.get('rootCause'):
            formatted['content']['rootCause'] = article_data['rootCause']

        if article_data.get('links'):
            formatted['relatedLinks'] = self._parse_links(article_data['links'])

        return formatted

    def _parse_links(self, links_text: str) -> List[Dict]:
        """
        Parse related links from text format.

        Extracts URLs and creates link objects.
        """
        urls = re.findall(r'https?://[^\s]+', links_text)
        return [{'url': url} for url in urls]

    def link_kb_to_rfe(self, kb_id: str, rfe_id: str, report_file: str) -> bool:
        """
        Link a KB article to an RFE/Bug report.

        Args:
            kb_id: KB article ID (e.g., SOL123456)
            rfe_id: RFE/Bug ID (e.g., AAPRFE-1234)
            report_file: Path to RFE/Bug report markdown file

        Returns:
            True if linked successfully, False otherwise
        """
        try:
            # Read existing report
            with open(report_file, 'r') as f:
                report_content = f.read()

            # Create KB article link
            kb_url = f"https://access.redhat.com/solutions/{kb_id.replace('SOL', '')}"
            kb_link = f"\n\n## Related Knowledge Base Articles\n\n- [{kb_id}]({kb_url})\n"

            # Check if "Related Knowledge Base Articles" section exists
            if "## Related Knowledge Base Articles" in report_content:
                # Append to existing section
                report_content = report_content.replace(
                    "## Related Knowledge Base Articles",
                    f"## Related Knowledge Base Articles\n\n- [{kb_id}]({kb_url})"
                )
            else:
                # Add new section at the end
                report_content += kb_link

            # Write updated report
            with open(report_file, 'w') as f:
                f.write(report_content)

            print(f"✅ Linked KB article {kb_id} to {rfe_id}")
            return True

        except Exception as e:
            print(f"Error linking KB article: {e}")
            return False

    def get_kb_article(self, article_id: str) -> Optional[Dict]:
        """
        Fetch full details of a specific KB article.

        Args:
            article_id: KB article ID

        Returns:
            Dictionary with full article content
        """
        try:
            response = self.session.get(
                f"{self.kb_api_base}/content/{article_id}",
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            return {
                'id': data.get('id', ''),
                'title': data.get('title', ''),
                'product': data.get('product', ''),
                'type': data.get('documentKind', ''),
                'environment': data.get('content', {}).get('environment', ''),
                'issue': data.get('content', {}).get('issue', ''),
                'resolution': data.get('content', {}).get('resolution', ''),
                'rootCause': data.get('content', {}).get('rootCause', ''),
                'status': data.get('status', ''),
                'views': data.get('view_count', 0),
                'url': data.get('view_uri', ''),
                'lastModified': data.get('lastModifiedDate', ''),
            }

        except requests.RequestException as e:
            print(f"Error fetching KB article: {e}")
            return None


if __name__ == "__main__":
    import json
    import sys

    # When called from Electron, output JSON
    if len(sys.argv) > 1 and sys.argv[1] == '--search':
        kab = KABManager()
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        
        # Optional filters
        product = sys.argv[3] if len(sys.argv) > 3 else None
        article_type = sys.argv[4] if len(sys.argv) > 4 else None
        limit = int(sys.argv[5]) if len(sys.argv) > 5 else 100  # Default 100 results
        
        results = kab.search_kb_articles(query, product=product, article_type=article_type, limit=limit)
        print(json.dumps(results, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == '--recent':
        kab = KABManager()
        articles = kab.fetch_recent_kb_articles(limit=10)
        print(json.dumps(articles, indent=2))

    else:
        # Test mode - demonstrates Hydra API v2 integration
        print("Testing KAB Manager with Hydra API v2...", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

        kab = KABManager()

        print("\n[Test 1] Searching KB articles for 'multipath'...", file=sys.stderr)
        results = kab.search_kb_articles("multipath", product="Red Hat Enterprise Linux", limit=5)

        if results and results['numFound'] > 0:
            print(f"\n✅ Found {results['numFound']} total articles (showing {len(results['docs'])}):", file=sys.stderr)
            for i, article in enumerate(results['docs'], 1):
                print(f"\n{i}. {article['title']}", file=sys.stderr)
                print(f"   ID: {article['id']}", file=sys.stderr)
                print(f"   Product: {article['product']}", file=sys.stderr)
                print(f"   Type: {article['type']}", file=sys.stderr)
                print(f"   KCS State: {article.get('kcs_state', 'N/A')}", file=sys.stderr)
                print(f"   URL: {article['url']}", file=sys.stderr)

            # Output full JSON for GUI
            print("\n" + "=" * 60, file=sys.stderr)
            print("JSON Output:", file=sys.stderr)
            print(json.dumps(results, indent=2))
        else:
            print("❌ No articles found or API error occurred", file=sys.stderr)
            print("Make sure you are connected to Red Hat VPN and have a valid Portal token", file=sys.stderr)
            print(json.dumps(results, indent=2))

