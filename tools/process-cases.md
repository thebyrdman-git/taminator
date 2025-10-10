# process_cases.fish

**Purpose**: Batch process case numbers from CSV or text files, creating directory structures and running initial analysis for each case.

**Location**: `~/.local/bin/process_cases.fish`

**Usage**:
```bash
process_cases.fish <filename>
```

**Functionality**:

### Input File Support
- **CSV files** (*.csv): Extracts case numbers from the first column
- **Text files**: Uses each line as a case number
- Automatically detects file type by extension
- Filters out empty lines and header rows

### Processing Workflow
For each case number found:

1. **Directory Creation**: Creates subdirectory named after case number (if doesn't exist)
2. **Case Analysis**: Runs `rhcase analyze <case_num> --save-raw --skip-ai`
3. **Organization**: Maintains clean directory structure

### Key Features
- **Idempotent**: Safe to run multiple times (won't recreate existing directories)
- **Progress Reporting**: Shows detailed progress for each case
- **Error Handling**: Validates input file existence and case number extraction
- **CSV Compatibility**: Works directly with `rhcase list <account> -f csv` output

### Integration with PAI Workflow

Typical usage in TAM automation:
```bash
# Navigate to account's active casework
cd ~/Documents/rh/projects/tam-ocp/bny/casework/active/

# Get current active cases
rhcase list bny -f csv > active.csv

# Process all active cases (creates directories + initial analysis)
process_cases.fish active.csv
```

### Output Structure
Each case directory will contain:
- Raw case data from `rhcase analyze --save-raw`
- Case attachments and metadata
- Analysis artifacts (without AI processing due to `--skip-ai`)

### Performance Characteristics
- **Lightweight**: Skips AI analysis for speed during bulk processing
- **Raw Data Focus**: Prioritizes data collection over analysis
- **Parallel Safe**: Can be run simultaneously across different accounts

### Error Conditions
- **File not found**: Exits with clear error message
- **No case numbers**: Validates successful extraction before processing
- **rhcase failures**: Individual case failures don't stop batch processing

This tool is essential for maintaining synchronized local case structures with Red Hat Portal data, supporting the evidence-based TAM methodology by ensuring consistent data availability for analysis.