import { useClerk } from '@clerk/clerk-expo'
import * as Linking from 'expo-linking'
import { useRouter } from 'expo-router'
import { Text, TouchableOpacity } from 'react-native'

export const SignOutButton = () => {
  // Use `useClerk()` to access the `signOut()` function
  const { signOut } = useClerk()
  const router = useRouter()
  
  const handleSignOut = async () => {
    try {
      await signOut()
      // Redirect to your desired page
      router.replace('/(auth)/home')
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }
  return (
    <TouchableOpacity onPress={handleSignOut} className='px-4 py-2 bg-red-600 rounded-full'>
      <Text className='text-white'>Sair</Text>
    </TouchableOpacity>
  )
}

export default SignOutButton;