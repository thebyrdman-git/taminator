# TAM RFE Chat - Command Reference

## Quick Start

The most common commands:
- `show cases for [customer]` - View cases
- `show open cases for [customer]` - Active cases only  
- `generate report for [customer]` - Create report
- `help` - Full command list

## Report Generation

Create RFE/Bug reports with copy/paste OR auto-posting options:

```
generate report for Wells Fargo
create RFE report for TD Bank
make active case report for Westpac
generate both reports for JPMC
```

## Case Discovery

Search and filter cases:

```
show cases for Wells Fargo
show open cases for Westpac
find Ansible cases for Wells Fargo
list OpenShift cases for TD Bank from last month
show cases from last quarter
```

### Filter Options:
- **By SBR Group**: `Ansible`, `OpenShift`, `RHEL`, `Satellite`
- **By Time**: `last week`, `last month`, `last quarter`
- **By Status**: `open cases` (active only)

## Case Similarity

Find related cases:

```
find cases similar to 04244831
show me cases like case 04244835
cases similar to 04244831
```

## Meeting Preparation

Generate meeting materials:

```
prepare summary for Wells Fargo meeting
prepare meeting for TD Bank
create meeting materials for Westpac
```

## Trend Analysis

Analyze case patterns over time:

```
show trend for TD Bank
analyze Wells Fargo case patterns
what's the trend for Westpac OpenShift cases?
```

## Customer Health

View customer health metrics:

```
show health for Wells Fargo
customer health status for TD Bank
analyze Westpac performance
```

## Tips

- **Any Customer**: You can use any customer name - the tool will learn new ones
- **Mix Filters**: Combine options: `show Ansible cases for Wells Fargo last month`
- **Natural Language**: Simple commands work: `show cases`, `generate report`
- **Report Delivery**: Choose copy/paste markdown OR auto-posting to portal

## Customer Configuration

Customers are stored in `config/customers.conf`:
```
customer_key:Display Name:Account_Number:Group_ID
```

Example:
```
wellsfargo:Wells Fargo:838043:4357341
westpac:Westpac Banking Corporation:1363155:unknown
```

Add new customers by:
1. Manually editing `config/customers.conf`
2. Using the tool - it will prompt for details on first use

## Examples from User Testing

These commands all work:

```bash
# Basic case viewing
show cases for westpac
show open cases for Wells Fargo
find cases for TD Bank

# Report generation
generate report for westpac
create RFE report for Wells Fargo

# Meeting prep
prepare meeting for westpac
```

## Troubleshooting

**"I'm not sure I understood"**
- Check spelling of customer name
- Try simpler command: `show cases for [customer]`
- Type `help` for examples

**Customer not recognized**
- Add to `config/customers.conf`
- Tool will prompt for details on first use

**NLP not matching**
- Use key action words: `show`, `generate`, `find`, `prepare`
- Include customer name in query
- Type `help` for working examples

