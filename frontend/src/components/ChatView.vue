<template>
  <div class="dark-mode">
    <!-- Message Window -->
    <div class="message-window">
      <ul class="messages">
        <li v-for="message in messages" :key="message.id">
          <span class="user">{{ message.user }}:</span>
          <span class="content" v-html="message.content"></span>
        </li>
        <!-- Show loading spinner while sending message -->
        <div v-if="sendingMessage" class="spinner"></div>
      </ul>
    </div>

    <!-- Message Input Container -->
    <div class="message-input-container">
      <!-- Message Input -->
      <div class="message-input">
        <input type="text" v-model="newMessage" :disabled="sendingMessage" @keyup.enter="sendMessage" placeholder="Type your message..." />
        <button @click="sendMessage" :disabled="sendingMessage">
          <span v-if="!sendingMessage">Send</span>
          <span v-else>Sending...</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      newMessage: '',
      backendUrl: 'http://localhost:3000/',
      sendingMessage: false,
    };
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim()) return;
      this.sendingMessage = true;

      this.messages.push({
        id: 0,
        user: 'ME',
        content: this.newMessage,
      });

      try {
        const response = await fetch(this.backendUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: this.newMessage }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data);
          this.messages.push(data);
        } else {
          console.error('Error sending message:', await response.text());
        }
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        this.sendingMessage = false;
        this.newMessage = '';
      }
    },
  },
};
</script>

<style scoped>
.dark-mode {
  color: #ddd;
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.message-window {
  flex: 1;
  overflow-y: scroll;
  border: 1px solid #444;
  padding: 10px;
  padding-bottom: 100px;
  background-color: #222;
  color: #ddd;
}

.messages {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 16px;
  line-height: 1.5;
  white-space: pre-wrap;
}

.user {
  font-weight: bold;
  background-color: #3498db;
  padding: 2px 5px;
  border-radius: 5px;
  margin-right: 5px;
}

.content {
  margin-left: 20px;
}

.message-input-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
}

.message-input {
  display: flex;
  align-items: center;
  margin-left: 20px;
  margin-right: 20px;
  padding: 10px;
  background-color: #333;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #666;
  background-color: #333;
  color: #ddd;
  font-size: 16px;
  line-height: 1.5;
}

.message-input button {
  margin-left: 10px;
  margin-right: 20px;
  padding: 10px 20px;
  border: none;
  background-color: #3498db;
  color: white;
  cursor: pointer;
}

.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin-left: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
