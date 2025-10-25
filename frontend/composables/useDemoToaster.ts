// frontend/composables/useDemoToaster.ts

export const useDemoToaster = () => {
  // A global state to hold the current message
  const message = useState<string | null>('demo-toast-message', () => null);

  // A function to show a message
  const show = (msg: string) => {
    message.value = msg;

    // Automatically hide the message after 3 seconds
    setTimeout(() => {
      message.value = null;
    }, 3000); // 3-second duration
  };

  return {
    message,
    show,
  };
};