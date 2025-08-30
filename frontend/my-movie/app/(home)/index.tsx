import { SignOutButton } from '@/app/components/SignOutButton'
import { SignedIn, SignedOut, useUser } from '@clerk/clerk-expo'
import { Link } from 'expo-router'
import { Text, View } from 'react-native'

export default function Page() {
  const { user } = useUser()

  console.log(user)

  return (
    <>
      <SignedIn >
        <View className='flex-1 items-center justify-start gap-4 py-4'>
          <Text>Olá, {user?.emailAddresses[0].emailAddress}</Text>
          <SignOutButton />
        </View>
      </SignedIn>

      <SignedOut>
        <View className='flex-1 items-center justify-center gap-4 py-4'>
          <Link href="/(auth)/login">
            <Text>Login</Text>
          </Link>

          <Link href="/(auth)/cadastro">
            <Text>Cadastro</Text>
          </Link>
        </View>
      </SignedOut>
    </>
  )
}