import { useSignIn } from '@clerk/clerk-expo'
import { Link, useRouter } from 'expo-router'
import React from 'react'
import { Text, TextInput, TouchableOpacity, View } from 'react-native'

export default function Page() {
  const { signIn, setActive, isLoaded } = useSignIn()
  const router = useRouter()

  const [emailAddress, setEmailAddress] = React.useState('')
  const [password, setPassword] = React.useState('')

  // Handle the submission of the sign-in form
  const onSignInPress = async () => {
    if (!isLoaded) return

    // Start the sign-in process using the email and password provided
    try {
      const signInAttempt = await signIn.create({
        identifier: emailAddress,
        password,
      })

      // If sign-in process is complete, set the created session as active
      // and redirect the user
      if (signInAttempt.status === 'complete') {
        await setActive({ session: signInAttempt.createdSessionId })
        router.replace('/')
      } else {
        // If the status isn't complete, check why. User might need to
        // complete further steps.
        console.error(JSON.stringify(signInAttempt, null, 2))
      }
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }

  return (
    <View className='flex-1 items-center justify-start gap-4 py-4'>
      <Text className='font-bold'>Login</Text>

      <View className='flex flex-col w-64 gap-1'>
        <Text>E-mail</Text>
        <TextInput
          className='border border-gray-300 rounded px-4 py-2 w-64 outline-none focus:border-gray-600 placeholder:text-gray-400 placeholder:italic'
          autoCapitalize="none"
          value={emailAddress}
          placeholder="seuemail@email.com"
          onChangeText={(emailAddress) => setEmailAddress(emailAddress)}
        />
      </View>

      <View className='flex flex-col w-64 gap-1'>
        <Text>Senha</Text>
        <TextInput
          className='border border-gray-300 rounded px-4 py-2 w-64 outline-none focus:border-gray-600 placeholder:text-gray-400 placeholder:italic'
          value={password}
          placeholder="Senha"
          secureTextEntry={true}
          onChangeText={(password) => setPassword(password)}
        />
      </View>

      <TouchableOpacity onPress={onSignInPress} className='bg-purple-300 px-4 py-2 rounded'>
        <Text>Continuar</Text>
      </TouchableOpacity>
      
      <View className='flex-row'>
        <Text>Não possui uma conta?</Text>
        <Link href="/(auth)/cadastro" className='text-purple-800'>
          <Text> Cadastre-se</Text>
        </Link>
      </View>
    </View>
  )
}