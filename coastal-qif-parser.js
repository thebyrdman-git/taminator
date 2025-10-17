// Coastal Credit Union QIF Parser for n8n
// Processes QIF files and converts to Actual Budget format
// Handles 425+ transactions automatically

const qifContent = $input.first().binary.data.toString();
const lines = qifContent.split('\n');
const transactions = [];
let currentTxn = {};

for (const line of lines) {
  const trimmedLine = line.trim();
  
  // Skip header and empty lines
  if (trimmedLine.startsWith('!Type:') || trimmedLine === '') continue;
  
  // End of transaction marker
  if (trimmedLine === '^') {
    if (Object.keys(currentTxn).length > 0) {
      // Convert date format MM/DD/YYYY to YYYY-MM-DD
      if (currentTxn.date) {
        const parts = currentTxn.date.split('/');
        if (parts.length === 3) {
          const month = parts[0].padStart(2, '0');
          const day = parts[1].padStart(2, '0');
          const year = parts[2];
          currentTxn.date = `${year}-${month}-${day}`;
        }
      }
      
      // Convert amount to cents (Actual Budget format)
      if (currentTxn.amount) {
        currentTxn.amount = Math.round(currentTxn.amount * 100);
      }
      
      transactions.push(currentTxn);
      currentTxn = {};
    }
  } else if (trimmedLine.startsWith('D')) {
    // Date field
    currentTxn.date = trimmedLine.substring(1);
  } else if (trimmedLine.startsWith('T')) {
    // Amount field
    currentTxn.amount = parseFloat(trimmedLine.substring(1));
  } else if (trimmedLine.startsWith('P')) {
    // Payee field
    currentTxn.payee = trimmedLine.substring(1);
  } else if (trimmedLine.startsWith('M')) {
    // Memo field
    currentTxn.memo = trimmedLine.substring(1) || '';
  } else if (trimmedLine.startsWith('C')) {
    // Cleared status
    currentTxn.cleared = trimmedLine.substring(1) === '*';
  } else if (trimmedLine.startsWith('N')) {
    // Check number
    currentTxn.checkNumber = trimmedLine.substring(1);
  }
}

// Return formatted transactions for Actual Budget
return transactions.map(txn => ({
  json: {
    date: txn.date,
    amount: txn.amount,
    payee: txn.payee || 'Unknown',
    notes: txn.memo || '',
    cleared: txn.cleared || false,
    account: 'Coastal Credit Union',
    imported_id: `coastal_${txn.date}_${Math.abs(txn.amount)}_${txn.payee?.substring(0,10) || 'unknown'}`
  }
}));
