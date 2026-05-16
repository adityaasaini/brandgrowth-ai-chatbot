import { useState } from "react"
import axios from "axios"
import "./App.css"

function App() {

  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Namaste 👋 Main BrandGrowth AI assistant hun. Aapko kis cheez mein help chahiye?"
    }
  ])

  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {

    if (!input.trim()) return

    const userMessage = {
      role: "user",
      text: input
    }

    setMessages((prev) => [...prev, userMessage])

    const userInput = input

    setInput("")
    setLoading(true)

    try {

      const response = await axios.post(
        "http://localhost:8000/chat",
        {
          question: userInput
        }
      )

      const botMessage = {
        role: "bot",
        text: response.data.answer
      }

      setMessages((prev) => [...prev, botMessage])

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "⚠️ Server se connect nahi ho paaya."
        }
      ])
    }

    setLoading(false)
  }

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {
      sendMessage()
    }
  }

  return (

    <div className="main-container">

      {/* Background Glow */}
      <div className="bg-circle circle-1"></div>
      <div className="bg-circle circle-2"></div>

      {/* Chat Card */}
      <div className="chat-card">

        {/* Header */}
        <div className="chat-header">

          <div className="brand-logo">
            BG
          </div>

          <div className="header-text">
            <h1>BrandGrowth</h1>
            <p>AI Website Assistant</p>
          </div>

        </div>

        {/* Messages */}
        <div className="chat-body">

          {
            messages.map((msg, index) => (

              <div
                key={index}
                className={`message-row ${msg.role}`}
              >

                <div className={`message-box ${msg.role}`}>
                  {msg.text}
                </div>

              </div>
            ))
          }

          {
            loading && (

              <div className="message-row bot">

                <div className="message-box bot typing">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

              </div>
            )
          }

        </div>

        {/* Input */}
        <div className="chat-input-box">

          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
          >
            Send
          </button>

        </div>

      </div>

    </div>
  )
}

export default App