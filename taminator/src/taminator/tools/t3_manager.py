#!/usr/bin/env python3
"""
T3 (Technical Topic Torrent) Manager

Fetches, converts, and distributes T3 technical blog posts to customers.
Integrates with Igloo Software API (Red Hat Source platform).

API Details:
- Platform: Igloo Software
- Base URL: https://source.redhat.com
- API Endpoint: /.api2/api/v1/ (Igloo API v1)
- Authentication: JWT cookie (rh_jwt) + SSO session
- Requires: Red Hat VPN
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional
import markdown
import html2text
from bs4 import BeautifulSoup
import os
import sys


class T3Manager:
    """Manages T3 blog fetching, conversion, and distribution via Igloo API."""
    
    def __init__(self, portal_token: Optional[str] = None):
        """
        Initialize T3 Manager with Red Hat authentication.
        
        Args:
            portal_token: Red Hat Customer Portal API token (JWT).
                         If not provided, attempts to load from environment.
        """
        # Igloo API configuration (from T3 page source analysis)
        self.base_url = "https://source.redhat.com"
        self.api_base = f"{self.base_url}/.api2/api/v1"
        self.community_key = "10"  # The Source community
        self.t3_channel_id = "3c8f877a-491b-4e5a-91cb-b52a2038b77c"  # T3 Blog channel
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Taminator/1.7.1 T3Manager',
            'Accept': 'application/json'
        })
        
        # Set authentication token (same as KB API - rh_jwt cookie)
        token = portal_token or os.getenv('RH_PORTAL_TOKEN')
        if token:
            self.session.cookies.set('rh_jwt', token, domain='source.redhat.com')
        
        # Note: Requires Red Hat VPN/Kerberos authentication
    
    def _get_mock_t3_posts(self) -> List[Dict]:
        """
        Return mock T3 blog posts for demo/testing when authentication isn't available.
        
        Returns:
            List of mock blog post dictionaries
        """
        return [
            {
                'title': 'Ansible Automation Platform 2.6 Performance Tuning Guide',
                'url': 'https://source.redhat.com/groups/public/t3/technical_topic_torrent_blog/ansible_automation_platform_26_performance_tuning_guide',
                'date': '2025-10-15',
                'scope': 'Customer',
                'severity': 'High',
                'description': 'Comprehensive guide to optimizing AAP 2.6 for enterprise workloads including job scheduling, database tuning, and resource allocation best practices.'
            },
            {
                'title': 'RHEL 9.5 Security Hardening Checklist',
                'url': 'https://source.redhat.com/groups/public/t3/technical_topic_torrent_blog/rhel_95_security_hardening_checklist',
                'date': '2025-10-12',
                'scope': 'Customer',
                'severity': 'High',
                'description': 'Step-by-step security hardening procedures for RHEL 9.5 deployments including FIPS compliance, SELinux configuration, and audit logging.'
            },
            {
                'title': 'OpenShift Service Mesh: Production Deployment Patterns',
                'url': 'https://source.redhat.com/groups/public/t3/technical_topic_torrent_blog/openshift_service_mesh_production_deployment_patterns',
                'date': '2025-10-08',
                'scope': 'Customer',
                'severity': 'Medium',
                'description': 'Real-world deployment patterns for OpenShift Service Mesh including multi-cluster federation, mTLS configuration, and observability integration.'
            },
            {
                'title': 'Troubleshooting AAP EDA Performance Issues',
                'url': 'https://source.redhat.com/groups/public/t3/technical_topic_torrent_blog/troubleshooting_aap_eda_performance_issues',
                'date': '2025-10-05',
                'scope': 'Internal',
                'severity': 'Medium',
                'description': 'Common performance bottlenecks in Event-Driven Ansible and proven troubleshooting methodologies including rulebook optimization and webhook debugging.'
            },
            {
                'title': 'Red Hat Satellite 6.16: What\'s New for TAMs',
                'url': 'https://source.redhat.com/groups/public/t3/technical_topic_torrent_blog/red_hat_satellite_616_whats_new_for_tams',
                'date': '2025-10-01',
                'scope': 'Internal',
                'severity': 'Low',
                'description': 'Overview of Satellite 6.16 new features including enhanced content views, improved subscription management, and REST API updates.'
            },
            {
                'title': '⚠️ Demo Data - Configure Portal Token in Auth Box',
                'url': '#auth-box',
                'date': '2025-10-22',
                'scope': 'Internal',
                'severity': 'Low',
                'description': 'This is sample data. To access real T3 posts:\n\n1. Open Auth Box (navigation menu)\n2. Save your Portal Token (rh_jwt cookie from browser)\n3. Click "Test" to verify authentication\n4. Return here and click "Refresh T3 Posts"\n\nThe token will be encrypted and stored securely in ~/.config/taminator/tokens.enc'
            }
        ]
    
    def fetch_latest_blogs_api(self, limit: int = 20, page: int = 1) -> Dict:
        """
        Fetch latest T3 blog posts via Igloo API (EXPERIMENTAL).
        
        This is a best-guess implementation based on Igloo platform patterns.
        May require adjustment after network traffic capture.
        
        Args:
            limit: Maximum number of blog posts to fetch (pageSize)
            page: Page number for pagination
            
        Returns:
            Dictionary with 'posts' list and 'pagination' info
        """
        try:
            # Attempt Igloo API call (best guess based on platform analysis)
            # Endpoint pattern: /.api2/api/v1/communities/{id}/channels/{id}/posts
            api_url = f"{self.api_base}/communities/{self.community_key}/channels/{self.t3_channel_id}/posts"
            
            params = {
                'page': page,
                'pageSize': limit,
                'sort': 'publishedDate:desc'  # Most recent first
            }
            
            print(f"[T3 API] Attempting: {api_url}", file=sys.stderr)
            print(f"[T3 API] Params: {params}", file=sys.stderr)
            
            response = self.session.get(api_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse Igloo API response (structure TBD - needs network capture)
            posts = []
            items = data.get('items', []) or data.get('posts', []) or data.get('docs', [])
            
            for item in items:
                # Extract post URL
                post_url = item.get('href', '') or item.get('url', '')
                if post_url and not post_url.startswith('http'):
                    post_url = f"{self.base_url}{post_url}"
                
                posts.append({
                    'id': item.get('id', ''),
                    'title': item.get('title', 'Untitled'),
                    'url': post_url,
                    'date': item.get('publishedDate', item.get('created', '')),
                    'author': item.get('author', {}).get('name', 'Red Hat'),
                    'author_id': item.get('author', {}).get('id', ''),
                    'description': item.get('summary', item.get('abstract', ''))[:300],
                    'views': item.get('viewCount', 0),
                    'comments': item.get('commentCount', 0),
                    'scope': 'TBD',  # Extracted from full content
                    'severity': 'Informational',
                    'fetched_at': datetime.now().isoformat()
                })
            
            return {
                'posts': posts,
                'pagination': {
                    'page': page,
                    'pageSize': limit,
                    'total': len(posts)
                }
            }
            
        except requests.RequestException as e:
            print(f"[T3 API] Error: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                print(f"[T3 API] Status: {e.response.status_code}", file=sys.stderr)
                print(f"[T3 API] Response: {e.response.text[:500]}", file=sys.stderr)
            print("[T3 API] Falling back to HTML scraping...", file=sys.stderr)
            return {'posts': [], 'pagination': {}}
    
    def fetch_latest_blogs(self, limit: int = 20) -> List[Dict]:
        """
        Fetch latest T3 blog posts from Red Hat Source.
        
        Tries Igloo API first, falls back to HTML scraping if API fails.
        
        Args:
            limit: Maximum number of blog posts to fetch
            
        Returns:
            List of blog post dictionaries with title, url, date, scope, severity, description
        """
        # Try API approach first (requires network capture to verify endpoint)
        api_result = self.fetch_latest_blogs_api(limit=limit)
        if api_result and api_result.get('posts'):
            print(f"✅ [T3] Fetched {len(api_result['posts'])} posts via API", file=sys.stderr)
            return api_result['posts']
        
        # Fallback to HTML scraping
        print("⚠️ [T3] Using HTML scraping fallback", file=sys.stderr)
        try:
            t3_blog_url = f"{self.base_url}/groups/public/t3/technical_topic_torrent_blog"
            response = self.session.get(t3_blog_url, timeout=10)
            
            # Check if we got redirected to login (authentication required)
            if response.status_code == 302 or '?signin' in response.url or 'login' in response.url.lower():
                print("⚠️ [T3] Authentication required - returning mock data for demo", file=sys.stderr)
                return self._get_mock_t3_posts()
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            blogs = []
            
            # Find blog post containers in Source (Igloo platform)
            # Look for jive-content-preview or similar structures
            blog_posts = soup.find_all('div', class_='jive-content-preview', limit=limit)
            
            if not blog_posts:
                # Fallback: look for any article-like structures
                blog_posts = soup.find_all(['article', 'div'], class_=['post', 'entry', 'content-item'], limit=limit)
                
            # If still no posts found, return mock data
            if not blog_posts:
                print("⚠️ [T3] No posts found in HTML - returning mock data for demo", file=sys.stderr)
                return self._get_mock_t3_posts()
            
            for post in blog_posts:
                try:
                    # Extract title
                    title_elem = post.find(['h2', 'h3', 'h4'], class_=['title', 'jive-link-title'])
                    title = title_elem.get_text(strip=True) if title_elem else "Untitled"
                    
                    # Extract URL
                    link_elem = title_elem.find('a', href=True) if title_elem else post.find('a', href=True)
                    url = link_elem['href'] if link_elem else ""
                    if url and not url.startswith('http'):
                        url = f"https://source.redhat.com{url}"
                    
                    # Extract date
                    date_elem = post.find('time') or post.find(class_=['date', 'timestamp'])
                    date_str = date_elem.get_text(strip=True) if date_elem else ""
                    
                    # Extract author
                    author_elem = post.find(class_=['author', 'username'])
                    author = author_elem.get_text(strip=True) if author_elem else "Red Hat"
                    
                    # Extract preview/description
                    desc_elem = post.find('div', class_=['preview', 'description', 'summary'])
                    description = desc_elem.get_text(strip=True)[:300] if desc_elem else ""
                    
                    blogs.append({
                        'title': title,
                        'url': url,
                        'date': date_str,
                        'author': author,
                        'description': description,
                        'scope': 'TBD',  # Extracted from full content
                        'severity': 'Informational',  # Extracted from full content
                        'fetched_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error parsing blog post: {e}")
                    continue
            
            return blogs
            
        except requests.RequestException as e:
            print(f"Error fetching T3 blogs: {e}")
            print("Note: T3 blog requires Red Hat VPN and authentication")
            return []
    
    def fetch_blog_content(self, blog_url: str) -> Optional[Dict]:
        """
        Fetch full content of a specific T3 blog post.
        
        T3 blog posts include:
        - Scope: Which customers it applies to
        - Severity: Informational, Critical, Important, etc.
        - Description: Full content
        
        Args:
            blog_url: URL of the blog post
            
        Returns:
            Dictionary with title, content (HTML), author, date, scope, severity
        """
        try:
            response = self.session.get(blog_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1') or soup.find(class_='jive-link-title')
            title = title_elem.get_text(strip=True) if title_elem else "Untitled"
            
            # Find main content area (Jive/Source specific)
            content_elem = soup.find('div', class_=['jive-rendered-content', 'jive-content-body'])
            if not content_elem:
                content_elem = soup.find('article') or soup.find(class_='content')
            content_html = str(content_elem) if content_elem else ""
            
            # Extract structured fields (Scope, Severity, Description)
            scope = "All Customers"
            severity = "Informational"
            
            # Look for structured content in the post
            if content_elem:
                text = content_elem.get_text()
                if 'Scope' in text:
                    scope_match = text.split('Scope')[-1].split('Severity')[0].strip()
                    scope = scope_match[:200] if scope_match else scope
                if 'Severity' in text:
                    severity_match = text.split('Severity')[-1].split('Description')[0].strip()
                    severity = severity_match[:50] if severity_match else severity
            
            # Extract metadata
            author_elem = soup.find(class_=['author', 'username']) or soup.find('span', class_='jive-username')
            author = author_elem.get_text(strip=True) if author_elem else "Red Hat"
            
            date_elem = soup.find('time') or soup.find(class_=['date', 'timestamp'])
            date = date_elem.get_text(strip=True) if date_elem else ""
            
            return {
                'title': title,
                'content_html': content_html,
                'author': author,
                'date': date,
                'scope': scope,
                'severity': severity,
                'url': blog_url
            }
            
        except requests.RequestException as e:
            print(f"Error fetching blog content: {e}")
            print("Note: T3 blog requires Red Hat VPN and authentication")
            return None
    
    def convert_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to markdown.
        
        Args:
            html_content: HTML string
            
        Returns:
            Markdown string
        """
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # Don't wrap lines
        
        markdown_content = h.handle(html_content)
        return markdown_content
    
    def format_for_email(self, blog_data: Dict) -> str:
        """
        Format blog content for email distribution (HTML).
        
        Args:
            blog_data: Blog data dictionary
            
        Returns:
            HTML formatted email content
        """
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Overpass', 'Open Sans', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #EE0000;
            border-bottom: 2px solid #EE0000;
            padding-bottom: 10px;
        }}
        .metadata {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        .content {{
            margin-top: 20px;
        }}
        a {{
            color: #0066CC;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
            font-size: 0.8em;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>{blog_data.get('title', 'Technical Topic')}</h1>
    
    <div class="metadata">
        <strong>Author:</strong> {blog_data.get('author', 'Red Hat')}<br>
        <strong>Date:</strong> {blog_data.get('date', '')}<br>
        <strong>Source:</strong> <a href="{blog_data.get('url', '')}">View original post</a>
    </div>
    
    <div class="content">
        {blog_data.get('content_html', '')}
    </div>
    
    <div class="footer">
        <p>This technical content was shared by your Red Hat Technical Account Manager.</p>
        <p>For more technical insights, visit <a href="https://access.redhat.com/blogs/766093/">Red Hat Technical Topic Torrent</a></p>
    </div>
</body>
</html>
"""
        return html_template
    
    def format_for_portal(self, blog_data: Dict) -> str:
        """
        Format blog content for Customer Portal group posting (Markdown).
        
        Args:
            blog_data: Blog data dictionary
            
        Returns:
            Markdown formatted portal content
        """
        markdown_content = f"""# {blog_data.get('title', 'Technical Topic')}

**Author:** {blog_data.get('author', 'Red Hat')}  
**Date:** {blog_data.get('date', '')}  
**Source:** [{blog_data.get('url', 'Red Hat Technical Blog')}]({blog_data.get('url', '')})

---

{self.convert_to_markdown(blog_data.get('content_html', ''))}

---

*This technical content was shared by your Red Hat Technical Account Manager.*  
*For more technical insights, visit [Red Hat Technical Topic Torrent](https://access.redhat.com/blogs/766093/)*
"""
        return markdown_content
    
    def get_blog_categories(self, blogs: List[Dict]) -> List[str]:
        """
        Extract unique categories/topics from blog titles.
        
        Args:
            blogs: List of blog dictionaries
            
        Returns:
            List of unique categories
        """
        categories = set()
        
        # Common Red Hat product keywords
        keywords = [
            'RHEL', 'OpenShift', 'Ansible', 'Satellite', 'OpenStack',
            'Storage', 'Virtualization', 'Container', 'Security',
            'Performance', 'Networking', 'Cloud'
        ]
        
        for blog in blogs:
            title = blog.get('title', '')
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    categories.add(keyword)
        
        return sorted(list(categories))


if __name__ == "__main__":
    import json
    import sys
    
    # When called from Electron, output JSON
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        t3 = T3Manager()
        blogs = t3.fetch_latest_blogs(limit=20)
        print(json.dumps(blogs, indent=2))
    else:
        # Test mode
        print("Testing T3 Manager...", file=sys.stderr)
        
        t3 = T3Manager()
        
        print("\nFetching latest blogs...", file=sys.stderr)
        blogs = t3.fetch_latest_blogs(limit=5)
        
        if blogs:
            print(f"\nFound {len(blogs)} blogs:", file=sys.stderr)
            for i, blog in enumerate(blogs, 1):
                print(f"\n{i}. {blog['title']}", file=sys.stderr)
                print(f"   Date: {blog['date']}", file=sys.stderr)
                print(f"   URL: {blog['url']}", file=sys.stderr)
                print(f"   Summary: {blog.get('description', '')[:100]}...", file=sys.stderr)
            
            # Output as JSON for GUI
            print(json.dumps(blogs, indent=2))
        else:
            print("No blogs found or error fetching", file=sys.stderr)
            print(json.dumps([]), file=sys.stderr)

