async function groupMessageHandler(message) {
  // Check if the message is from a group or supergroup
  if (message.chat.type === 'group' || message.chat.type === 'supergroup') {
    // Check if the message mentions the bot
    if (message.entities && message.entities.some(entity => entity.type === 'bot_command')) {
      // Check if the user is a member of your channel
      const user = await bot.getChatMember(process.env.CHANNEL_ID, message.from.id);
      if (user.status !== 'member') {
        // Prompt the user to join the channel before using the bot
        await bot.sendMessage(message.chat.id, 'Please join our channel to use this bot.');
      } else {
        // Process the message normally
        // ...
      }
    }
  }
}
