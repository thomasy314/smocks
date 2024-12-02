function snakeCaseToCamelCase<T extends Record<string, any>>(
  obj: T
): Record<string, any> {
  const toPascalCase = (str: string): string => {
    return str
      .split("_")
      .map((word, index) =>
        index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1)
      )
      .join("");
  };

  const result: Record<string, any> = {};

  for (const [key, value] of Object.entries(obj)) {
    const pascalCaseKey = toPascalCase(key);
    if (value && typeof value === "object" && !Array.isArray(value)) {
      // Recursively convert nested objects
      result[pascalCaseKey] = snakeCaseToCamelCase(value);
    } else {
      result[pascalCaseKey] = value;
    }
  }

  return result;
}

export { snakeCaseToCamelCase };
