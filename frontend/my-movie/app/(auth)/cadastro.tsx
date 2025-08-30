import { useSignUp } from '@clerk/clerk-expo'
import { Link, useRouter } from 'expo-router'
import * as React from 'react'
import { Text, TextInput, TouchableOpacity, View } from 'react-native'

export default function Cadastro() {
  const { isLoaded, signUp, setActive } = useSignUp()
  const router = useRouter()

  const [emailAddress, setEmailAddress] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [pendingVerification, setPendingVerification] = React.useState(false)
  const [code, setCode] = React.useState('')

  // Handle submission of sign-up form
  const onSignUpPress = async () => {
    if (!isLoaded) return

    // Start sign-up process using email and password provided
    try {
      await signUp.create({
        emailAddress,
        password,
      })

      // Send user an email with verification code
      await signUp.prepareEmailAddressVerification({ strategy: 'email_code' })

      // Set 'pendingVerification' to true to display second form
      // and capture OTP code
      setPendingVerification(true)
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }

  // Handle submission of verification form
  const onVerifyPress = async () => {
    if (!isLoaded) return

    try {
      // Use the code the user provided to attempt verification
      const signUpAttempt = await signUp.attemptEmailAddressVerification({
        code,
      })

      // If verification was completed, set the session to active
      // and redirect the user
      if (signUpAttempt.status === 'complete') {
        await setActive({ session: signUpAttempt.createdSessionId })
        router.replace('/')
      } else {
        // If the status is not complete, check why. User may need to
        // complete further steps.
        console.error(JSON.stringify(signUpAttempt, null, 2))
      }
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }

  if (pendingVerification) {
    return (
      <>
        <Text>Verify your email</Text>
        <TextInput
          value={code}
          placeholder="Enter your verification code"
          onChangeText={(code) => setCode(code)}
        />
        <TouchableOpacity onPress={onVerifyPress}>
          <Text>Verify</Text>
        </TouchableOpacity>
      </>
    )
  }

  return (
    <View className='flex-1 items-center justify-start gap-4 py-4'>

      <Text className='font-bold'>Cadastro</Text>

      <View className='flex flex-col w-64 gap-1'>
        <Text>E-mail</Text>
        <TextInput
          className='border border-gray-300 rounded px-4 py-2 w-64 outline-none focus:border-gray-600 placeholder:text-gray-400 placeholder:italic'
          autoCapitalize="none"
          value={emailAddress}
          placeholder="seuemail@email.com"
          onChangeText={(email) => setEmailAddress(email)}
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

      <TouchableOpacity onPress={onSignUpPress} className='bg-purple-300 px-4 py-2 rounded'>
        <Text>Continuar</Text>
      </TouchableOpacity>
      <View className='flex-row'>
        <Text>Já possui uma conta?</Text>
        <Link href="/(auth)/login" className='text-purple-800'>
          <Text> Login</Text>
        </Link>
      </View>
    </View>
  )
}