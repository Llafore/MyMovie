import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';
import { ClerkProvider } from '@clerk/clerk-expo';
import { tokenCache } from '@clerk/clerk-expo/token-cache';
import '../global.css';

import { Slot } from 'expo-router';

export default function RootLayout() {
  return (
    <ClerkProvider tokenCache={tokenCache}>
      <GluestackUIProvider mode="dark">
        <Slot/>
      </GluestackUIProvider>
    </ClerkProvider>
  );
}

