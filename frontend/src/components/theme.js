// theme.js
import { extendTheme } from "@chakra-ui/react";

const customTheme = extendTheme({
  fonts: {
    heading: `'Inter', sans-serif`,  // Use Inter for headings
    body: `'Inter', sans-serif`,     // Use Inter for body text
  },
});

export default customTheme;