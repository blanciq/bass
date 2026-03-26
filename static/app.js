const API = '';

function chatApp() {
    return {
        conversations: [],
        activeId: null,
        activeConversation: null,
        messageInput: '',
        sending: false,

        async init() {
            await this.loadConversations();
        },

        async loadConversations() {
            const res = await fetch(`${API}/conversations`);
            this.conversations = await res.json();
        },

        async createConversation() {
            const res = await fetch(`${API}/conversations`, { method: 'POST' });
            const conv = await res.json();
            this.conversations.unshift(conv);
            await this.selectConversation(conv.id);
        },

        async selectConversation(id) {
            this.activeId = id;
            const res = await fetch(`${API}/conversations/${id}`);
            this.activeConversation = await res.json();
            this.$nextTick(() => this.scrollToBottom());
        },

        async deleteConversation(id) {
            await fetch(`${API}/conversations/${id}`, { method: 'DELETE' });
            this.conversations = this.conversations.filter(c => c.id !== id);
            if (this.activeId === id) {
                this.activeId = null;
                this.activeConversation = null;
            }
        },

        async sendMessage() {
            const content = this.messageInput.trim();
            if (!content || this.sending) return;

            this.messageInput = '';
            this.sending = true;

            // optimistic user message
            this.activeConversation.messages.push({
                id: crypto.randomUUID(),
                role: 'user',
                content: content,
                created_at: new Date().toISOString()
            });
            this.$nextTick(() => this.scrollToBottom());

            try {
                const res = await fetch(`${API}/conversations/${this.activeId}/messages`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content })
                });
                const msg = await res.json();
                this.activeConversation.messages.push(msg);
            } catch (e) {
                this.activeConversation.messages.push({
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    content: 'Something went wrong. Please try again.',
                    created_at: new Date().toISOString()
                });
            } finally {
                this.sending = false;
                this.$nextTick(() => this.scrollToBottom());
            }
        },

        scrollToBottom() {
            const container = this.$refs.messagesContainer;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        },

        formatTime(iso) {
            if (!iso) return '';
            const d = new Date(iso);
            return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        },

        autoResize(event) {
            const el = event.target;
            el.style.height = 'auto';
            el.style.height = Math.min(el.scrollHeight, 120) + 'px';
        }
    };
}
