import { useAuth } from '@clerk/clerk-expo'
import { Redirect, Stack } from 'expo-router'

export default function AuthRoutesLayout() {
  const { isSignedIn } = useAuth()
  console.log("no layout")

  if (isSignedIn) {
    return <Redirect href={'/'} />
  }

  return (
    <Stack
      screenOptions={{
        animationMatchesGesture: true,
        contentStyle: { backgroundColor: 'black' },
        headerShown: false,
        presentation: 'transparentModal',
        animationDuration: 100,
        animation: 'fade_from_bottom',
        animationTypeForReplace: 'push',
      }}
    />
  );
}
