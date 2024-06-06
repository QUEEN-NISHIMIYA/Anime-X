const groupMessageHandler = async (message) => {
  const responding_msg = message.reply_to_message ? message.reply_to_message : message;
  const imageURL = await getImageFromMessage(responding_msg);
  if (!imageURL) {
    if (responding_msg.text?.toLowerCase().includes("/help")) {
      return await sendMessage(message.chat.id, getHelpMessage(app.locals.botName), {
        reply_to_message_id: message.message_id,
        parse_mode: "Markdown",
      });
    }
    // cannot find image from the message mentioning the bot
    return await sendMessage(
      message.chat.id,
      "Mention me in an anime screenshot, I will tell you what anime is that",
      { reply_to_message_id: message.message_id },
    );
  }
  setMessageReaction(message.chat.id, message.message_id, ["👌"]);
  const result = await submitSearch(imageURL, responding_msg, message);
  sendChatAction(message.chat.id, "typing");
  setMessageReaction(message.chat.id, message.message_id, ["👍"]);

  if (result.isAdult) {
    await sendMessage(
      message.chat.id,
      "I've found an adult result 😳\nPlease forward it to me via Private Chat 😏",
      {
        reply_to_message_id: responding_msg.message_id,
      },
    );
    return;
  }

  if (result.video && !messageIsSkipPreview(message)) {
    const videoLink = messageIsMute(message) ? ${result.video}&mute : result.video;
    const video = await fetch(videoLink, { method: "HEAD" });
    if (video.ok && video.headers.get("content-length") > 0) {
      await sendVideo(message.chat.id, videoLink, {
        caption: result.text,
        has_spoiler: responding_msg.has_media_spoiler,
        parse_mode: "Markdown",
        reply_to_message_id: responding_msg.message_id,
      });
      return;
    }
  }

  await sendMessage(message.chat.id, result.text, {
    parse_mode: "Markdown",
    reply_to_message_id: responding_msg.message_id,
  });
};

app.post("/", async (req, res) => {
  const message = req.body?.message;
  if (message?.chat?.type === "private") {
    await privateMessageHandler(message);
    setMessageReaction(message.chat.id, message.message_id, []);
  } else if (message?.chat?.type === "group" || message?.chat?.type === "supergroup") {
    if (messageIsMentioningBot(message)) {
      await groupMessageHandler(message);
      setMessageReaction(message.chat.id, message.message_id, []);
    }
  }
  res.sendStatus(204);
});

app.get("/", (req, res) => {
  return res.send(
    <meta http-equiv="Refresh" content="0; URL=https://t.me/${app.locals.botName ?? ""}">,
  );
});

app.listen(PORT, "0.0.0.0", () => console.log(server listening on port ${PORT}));
