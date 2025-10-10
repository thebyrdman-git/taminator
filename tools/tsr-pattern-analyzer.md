# tsr-pattern-analyzer

Identify recurring issue patterns and case categorization for Technical Service Reviews.

## Location
`~/.local/bin/tsr-pattern-analyzer.py`

## Description
Advanced pattern recognition system for Technical Service Review analysis. Identifies recurring technical issues, categorizes cases by business impact, and provides insights into customer environment patterns and support needs.

## Key Features
- **OpenShift-Specific Patterns**: Pre-configured patterns for OpenShift, ACM, Pipelines, etc.
- **Business Impact Classification**: Categorizes cases by business criticality
- **Complexity Assessment**: Identifies high-complexity cases requiring specialist attention
- **Trend Detection**: Recognizes emerging patterns and recurring issues
- **Root Cause Grouping**: Groups related cases for holistic problem-solving

## Commands

### Basic Usage
```bash
tsr-pattern-analyzer.py <account_name>                  # Analyze case patterns
tsr-pattern-analyzer.py <account_name> --data-dir /path # Custom data directory
```

### Examples
```bash
# Analyze Discover case patterns
tsr-pattern-analyzer.py discover

# Analyze with custom data source
tsr-pattern-analyzer.py cibc --data-dir extracted-data/

# Generate detailed pattern report
tsr-pattern-analyzer.py citi --verbose --include-examples
```

## Pattern Categories

### Technical Issue Types
- **Authentication**: OAuth, LDAP, SSO, Kerberos issues
- **Networking**: DNS, connectivity, firewall, proxy, ingress problems
- **Storage**: PVC, PV, NFS, Ceph, disk-related issues
- **Performance**: CPU, memory, latency, resource constraints
- **Upgrade**: Version updates, migration, cluster upgrades
- **Installation**: Deployment, bootstrap, setup issues
- **Monitoring**: Alerts, Prometheus, Grafana, metrics problems
- **Pipeline**: Tekton, CI/CD, build failures
- **Operator**: CRD, custom resource, controller issues
- **ETCD**: Backup, restore, cluster state problems

### Business Impact Categories
- **Business Critical**: Production outages, critical system failures
- **Performance Impact**: Degraded performance affecting operations
- **Functional Issue**: Features not working as expected
- **Informational**: Questions, guidance requests, documentation needs

### Complexity Classification
- **High**: >20 comments, multiple specialists, extended resolution
- **Medium**: 10-19 comments, standard technical complexity
- **Low**: <10 comments, straightforward resolution

## Analysis Outputs

### Pattern Distribution Report
- **Issue Type Frequency**: Most common technical problems
- **Business Impact Distribution**: Critical vs non-critical case ratios
- **Complexity Patterns**: Resource-intensive cases identification
- **Seasonal Trends**: Time-based pattern recognition

### Recurring Issue Identification
- **Root Cause Grouping**: Related cases grouped by underlying cause
- **Prevention Opportunities**: Issues that could be prevented proactively
- **Knowledge Gaps**: Areas where documentation or training could help
- **Environment Patterns**: Infrastructure-related recurring issues

## Report Generation

### Executive Summary
```markdown
# Case Pattern Analysis - [Account]

## Top Issue Categories
1. Authentication: 15 cases (23.4%)
2. Networking: 12 cases (18.7%)
3. Performance: 10 cases (15.6%)

## Complexity Distribution
- High: 8 cases (specialist engagement recommended)
- Medium: 35 cases (standard support)
- Low: 21 cases (quick resolution)

## Recommendations
- Focus on authentication best practices
- Proactive network configuration review
- Performance monitoring implementation
```

### Detailed Analysis
- **Case Examples**: Specific case numbers for each pattern
- **Timeline Analysis**: When patterns emerge and resolve
- **Resolution Patterns**: How different issue types are typically resolved
- **Customer Impact**: Business impact assessment for each pattern

## Integration Points

### Input Sources
- **tsr-case-extractor**: Requires extracted case data
- **Case JSON Files**: Processes rhcase output format
- **Comment Analysis**: Analyzes case comment text for patterns

### Output Integration
- **tsr-report-generator**: Pattern data for executive summaries
- **Business Intelligence**: Structured data for dashboards
- **Process Improvement**: Insights for support process optimization
- **Training Materials**: Pattern data for team training development

## Pattern Recognition Algorithm

### Text Analysis
- **Keyword Matching**: Advanced regex patterns for issue identification
- **Context Awareness**: Considers surrounding text for accurate categorization
- **Weighted Scoring**: Multiple keyword matches increase confidence
- **False Positive Reduction**: Filters out irrelevant pattern matches

### Statistical Analysis
- **Frequency Analysis**: Identifies statistically significant patterns
- **Correlation Detection**: Finds relationships between different issue types
- **Trend Analysis**: Recognizes emerging or declining patterns
- **Significance Testing**: Validates pattern importance

## Advanced Features

### Custom Pattern Definition
```python
# Add custom patterns for specific customer environments
custom_patterns = {
    'customer_specific': ['custom_app', 'special_config', 'unique_setup']
}
```

### Multi-Account Comparison
```bash
# Compare patterns across accounts
tsr-pattern-analyzer.py --compare cibc,citi,discover
```

### Temporal Analysis
```bash
# Analyze pattern evolution over time
tsr-pattern-analyzer.py discover --timeline --quarters 4
```

## Use Cases

### TAM Account Planning
- **Environment Assessment**: Understand customer infrastructure challenges
- **Proactive Strategy**: Plan preventive measures based on patterns
- **Resource Allocation**: Predict support resource needs
- **Training Planning**: Identify customer training opportunities

### Customer Engagement
- **Pattern Sharing**: Discuss recurring issues with customer
- **Prevention Planning**: Collaborate on issue prevention strategies
- **Best Practices**: Share practices to avoid common problems
- **Strategic Discussions**: Use patterns to guide technical roadmap

### Process Improvement
- **Support Optimization**: Improve support processes based on patterns
- **Knowledge Base Enhancement**: Create documentation for common issues
- **Training Programs**: Develop training based on recurring problems
- **Tool Development**: Build tools to address common pattern categories

## Integration with PAI Tools

### Workflow Integration
```bash
# Complete pattern analysis workflow
tsr-case-extractor.py discover
tsr-pattern-analyzer.py discover
tsr-report-generator.py discover
```

### PAI Tool Chain
- **pai-audit**: Logs pattern analysis for compliance
- **pai-search**: Stores pattern insights in knowledge base
- **fabric**: Uses patterns for AI-enhanced analysis

## Output Examples

### Issue Type Summary
```
Authentication Issues: 23 cases
├── OAuth integration: 12 cases
├── LDAP connectivity: 7 cases  
└── SSO configuration: 4 cases

Networking Issues: 18 cases
├── DNS resolution: 8 cases
├── Firewall rules: 6 cases
└── Ingress configuration: 4 cases
```

### Business Impact Assessment
```
High Business Impact: 15 cases
├── Production outages: 8 cases
├── Critical system failures: 4 cases
└── Revenue-affecting issues: 3 cases
```