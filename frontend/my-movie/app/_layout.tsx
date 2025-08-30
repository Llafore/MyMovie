import { ClerkProvider } from '@clerk/clerk-expo';
import { tokenCache } from '@clerk/clerk-expo/token-cache';
import { ptBR } from '@clerk/localizations';
import { Slot } from "expo-router";
import "../styles.css";

export default function RootLayout() {
    
  return (
    <ClerkProvider localization={ptBR} tokenCache={tokenCache}>
      <Slot />
    </ClerkProvider>
  )
}
