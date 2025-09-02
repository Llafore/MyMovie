import { SignOutButton } from '@/app/components/SignOutButton'
import { SignedIn, SignedOut, useUser } from '@clerk/clerk-expo'
import { Link } from 'expo-router'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

export default function Page() {
  const { user } = useUser()

  console.log(user)

  return (
      <SafeAreaView edges={['top']} className='flex-1 items-center justify-start gap-4 py-4 bg-black'>
        <SignedIn >
          <View className='flex-1 items-center justify-start gap-4 py-4 bg-black'>
            <Text className='text-white'>Olá, {user?.emailAddresses[0].emailAddress}</Text>
            <SignOutButton />
          </View>
        </SignedIn>
        <SignedOut>
          <View className='flex-1 items-center justify-center gap-4 py-4 bg-black'>
            <Link href="/login">
              <Text className='text-white'>Login</Text>
            </Link>

            <Link href="/(auth)/cadastro">
              <Text className='text-white'>Cadastro</Text>
            </Link>
          </View>
        </SignedOut>
      </SafeAreaView>


  )
}