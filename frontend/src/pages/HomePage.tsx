import { Link } from "react-router-dom";

export default function HomePage() {
  const features = [
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      ),
      title: "Smart Conversations",
      description: "Natural language processing for seamless product discovery and shopping assistance."
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
      title: "Product Search",
      description: "Find products quickly with intelligent search powered by AI and semantic understanding."
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      title: "Instant Responses",
      description: "Get immediate answers to your questions about products, prices, and availability."
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
      ),
      title: "Personalized Help",
      description: "Get tailored recommendations based on your preferences and shopping history."
    }
  ];

  const categories = [
    { name: "📱 Mobile Phones", query: "Show me the best mobile phones" },
    { name: "👟 Shoes", query: "What shoes do you have?" },
    { name: "👔 Shirts", query: "Show me some shirts" },
    { name: "⌚ Watches", query: "I'm looking for watches" },
    { name: "📷 Cameras", query: "Show me cameras" }
  ];

  return (
    <div className="min-h-dvh flex flex-col bg-black text-zinc-100">
      {/* Header */}
      <header className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h1 className="text-lg font-bold text-zinc-100">E-Commerce Chatbot</h1>
          </div>
          <Link 
            to="/chat" 
            className="rounded-lg px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 transition-colors"
          >
            Start Chat
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="flex-1">
        <div className="mx-auto max-w-6xl px-4 py-16 md:py-24">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center gap-2 rounded-full border border-zinc-800 bg-zinc-900/50 px-4 py-1.5 text-sm text-zinc-400 mb-6">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              AI-Powered Shopping Assistant
            </div>
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-white mb-6">
              Your Personal
              <span className="bg-linear-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"> Shopping </span>
              Assistant
            </h2>
            <p className="text-lg md:text-xl text-zinc-400 mb-8 max-w-2xl mx-auto">
              Discover products, get recommendations, and find the best deals with our chatbot. 
              Ask anything about our product catalog!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/chat" 
                className="inline-flex items-center justify-center gap-2 rounded-xl px-6 py-3 text-base font-semibold text-white bg-indigo-600 hover:bg-indigo-500 transition-all hover:scale-105"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                Start Chatting
              </Link>
              <a 
                href="#features" 
                className="inline-flex items-center justify-center gap-2 rounded-xl px-6 py-3 text-base font-semibold text-zinc-200 bg-zinc-800 hover:bg-zinc-700 transition-colors"
              >
                Learn More
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Categories */}
          <div className="mt-16">
            <p className="text-center text-sm text-zinc-500 mb-4">Popular Categories</p>
            <div className="flex flex-wrap gap-3 justify-center">
              {categories.map((category) => (
                <Link
                  key={category.name}
                  to={`/chat?q=${encodeURIComponent(category.query)}`}
                  className="rounded-full border border-zinc-800 bg-zinc-900/50 px-4 py-2 text-sm text-zinc-300 hover:border-indigo-500/50 hover:bg-zinc-800 transition-colors"
                >
                  {category.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="border-t border-zinc-800 bg-zinc-950/50">
        <div className="mx-auto max-w-6xl px-4 py-16 md:py-24">
          <div className="text-center mb-12">
            <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">Why Choose Our Chatbot?</h3>
            <p className="text-zinc-400 max-w-xl mx-auto">Experience the shopping with AI-powered assistance that understands your needs.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div 
                key={index}
                className="rounded-2xl border border-zinc-800 bg-zinc-900/30 p-6 hover:border-zinc-700 transition-colors group"
              >
                <div className="w-12 h-12 rounded-xl bg-indigo-600/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4 group-hover:bg-indigo-600/20 transition-colors">
                  {feature.icon}
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">{feature.title}</h4>
                <p className="text-sm text-zinc-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-zinc-800">
        <div className="mx-auto max-w-6xl px-4 py-16">
          <div className="rounded-2xl border border-zinc-800 bg-linear-to-br from-indigo-600/10 via-zinc-900 to-purple-600/10 p-8 md:p-12 text-center">
            <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">Ready to Start Shopping?</h3>
            
            <Link 
              to="/chat" 
              className="inline-flex items-center justify-center gap-2 rounded-xl px-8 py-4 text-lg font-semibold text-white bg-indigo-600 hover:bg-indigo-500 transition-all hover:scale-105"
            >
              Start a Conversation
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-800 bg-zinc-950">
        <div className="mx-auto max-w-6xl px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-zinc-500 text-sm">
              <div className="w-6 h-6 rounded bg-indigo-600 flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              E-Commerce Chatbot
            </div>
            <p className="text-zinc-600 text-sm">
              Powered by AI • © 2026 All rights reserved
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
