import { Heading } from "@/components/ui/heading";
import { useSignIn } from "@clerk/clerk-expo";
import React, { useState } from "react";
import { Button, Text, TextInput } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ForgotPasswordScreen() {
  const { signIn, setActive } = useSignIn();
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [step, setStep] = useState<"request" | "verify">("request");

  const requestReset = async () => {
    try {
      await signIn!.create({
        strategy: "reset_password_email_code",
        identifier: email,
      });
      setStep("verify");
    } catch (err: any) {
      console.error("Request error:", err.errors || err);
    }
  };

  const verifyReset = async () => {
    try {
      const result = await signIn!.attemptFirstFactor({
        strategy: "reset_password_email_code",
        code,
        password,
      });

      if (result.status === "complete") {
        await setActive!({ session: result.createdSessionId });
      }
    } catch (err: any) {
      console.error("Verify error:", err.errors || err);
    }
  };

  return (
    <SafeAreaView className="flex-1 items-center justify-start gap-6 p-4 bg-black">
      <Heading size={'3xl'} className='text-white'>Forgot password</Heading>

      {step === "request" && (
        <>
          <Text className="text-white">Enter your email</Text>
          <TextInput
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            className="border border-gray-500 rounded p-4 w-full outline-none focus:border-gray-300 placeholder:text-gray-400 placeholder:italic text-white"
          />
          <Button title="Send reset code" onPress={requestReset} />
        </>
      )}

      {step === "verify" && (
        <>
          <Text className="text-white">Enter the code sent to your email and your new password</Text>
          <TextInput
            placeholder="Code"
            value={code}
            onChangeText={setCode}
            className="border border-gray-500 rounded p-4 w-full outline-none focus:border-gray-300 placeholder:text-gray-400 placeholder:italic text-white"
          />
          <TextInput
            placeholder="New password"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
            className="border border-gray-500 rounded p-4 w-full outline-none focus:border-gray-300 placeholder:text-gray-400 placeholder:italic text-white"
          />
          <Button title="Reset password" onPress={verifyReset} />
        </>
      )}
    </SafeAreaView>
  );
}
