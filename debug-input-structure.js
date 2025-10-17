// Debug code to see what input structure we have
// Replace the QIF parser temporarily with this

console.log("=== INPUT DEBUG ===");
console.log("Full input:", JSON.stringify($input.all(), null, 2));

if ($input.first()) {
  console.log("First item exists");
  console.log("First item keys:", Object.keys($input.first()));
  
  if ($input.first().binary) {
    console.log("Binary data exists:", Object.keys($input.first().binary));
  } else {
    console.log("No binary data found");
  }
  
  if ($input.first().json) {
    console.log("JSON data exists:", $input.first().json);
  }
  
  if ($input.first().data) {
    console.log("Direct data exists:", typeof $input.first().data);
  }
} else {
  console.log("No input items found");
}

return [{
  json: {
    debug: "Check console for input structure",
    inputCount: $input.all().length,
    hasFirst: !!$input.first(),
    hasBinary: !!($input.first() && $input.first().binary),
    hasData: !!($input.first() && $input.first().data)
  }
}];
