setTimeout(() => {
    const chatBox = window.parent.document.getElementById("chat-box");
    if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
}, 100);
