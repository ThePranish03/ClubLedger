import { useWallet } from '@txnlab/use-wallet-react'
import React, { useState } from 'react'
import ConnectWallet from './components/ConnectWallet'

const Home: React.FC = () => {
  const { activeAddress } = useWallet()
  const [openWalletModal, setOpenWalletModal] = useState(false)

  const [eventName, setEventName] = useState('')
  const [sponsorName, setSponsorName] = useState('')
  const [amount, setAmount] = useState('')
  const [sponsors, setSponsors] = useState<any[]>([])
  const [transactions, setTransactions] = useState<any[]>([])
  const [verified, setVerified] = useState(false)
  const [error, setError] = useState('')

  const handleSponsor = () => {
    setError('')

    if (!activeAddress) {
      setError('Please connect your wallet first.')
      return
    }

    if (!eventName || !sponsorName || !amount) {
      setError('All fields are required.')
      return
    }

    if (Number(amount) <= 0) {
      setError('Amount must be greater than zero.')
      return
    }

    // Mock transaction (replace with Flask later)
    const txId = 'TX' + Math.floor(Math.random() * 1000000)

    setSponsors([...sponsors, { sponsorName, amount }])
    setTransactions([...transactions, { txId, amount }])
    setVerified(true)

    setSponsorName('')
    setAmount('')
  }

  const totalRaised = sponsors.reduce(
    (sum, s) => sum + Number(s.amount),
    0
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-10">

      <div className="max-w-4xl mx-auto">

        <h1 className="text-4xl font-bold mb-2">
          🎉 ClubLedger
        </h1>

        <p className="text-slate-300 mb-6">
          Transparent Blockchain-Based Event Finance System
        </p>

        {/* Wallet Button */}
        <button
          className="bg-indigo-600 px-4 py-2 rounded hover:bg-indigo-500 mb-6"
          onClick={() => setOpenWalletModal(true)}
        >
          {activeAddress ? 'Wallet Connected' : 'Connect Wallet'}
        </button>

        {/* Event Card */}
        <div className="bg-slate-700 p-6 rounded-xl shadow-lg mb-8">

          <h2 className="text-2xl font-semibold mb-4">
            📌 Create Sponsorship
          </h2>

          <input
            className="p-2 rounded text-black w-full mb-3"
            placeholder="Event Name"
            value={eventName}
            onChange={(e) => setEventName(e.target.value)}
          />

          <input
            className="p-2 rounded text-black w-full mb-3"
            placeholder="Sponsor Name"
            value={sponsorName}
            onChange={(e) => setSponsorName(e.target.value)}
          />

          <input
            type="number"
            className="p-2 rounded text-black w-full mb-3"
            placeholder="Amount (ALGO)"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />

          {error && (
            <div className="bg-red-600 p-2 rounded mb-3">
              {error}
            </div>
          )}

          <button
            onClick={handleSponsor}
            className="bg-cyan-500 px-4 py-2 rounded hover:bg-cyan-400 w-full"
          >
            Sponsor Event
          </button>

          {verified && (
            <div className="bg-green-600 px-3 py-1 rounded-full w-fit mt-4">
              ✅ Blockchain Verified
            </div>
          )}

        </div>

        {/* Summary Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Sponsors */}
          <div className="bg-slate-700 p-6 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">
              📢 Sponsors
            </h3>

            {sponsors.length === 0 && (
              <p className="text-slate-300">
                No sponsors yet.
              </p>
            )}

            <ul className="space-y-2">
              {sponsors.map((s, i) => (
                <li key={i} className="bg-slate-800 p-2 rounded">
                  {s.sponsorName} – {s.amount} ALGO
                </li>
              ))}
            </ul>

            <div className="mt-4 font-semibold">
              💰 Total Raised: {totalRaised} ALGO
            </div>
          </div>

          {/* Transactions */}
          <div className="bg-slate-700 p-6 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">
              📜 Transaction History
            </h3>

            {transactions.length === 0 && (
              <p className="text-slate-300">
                No transactions yet.
              </p>
            )}

            <ul className="space-y-2">
              {transactions.map((t, i) => (
                <li key={i} className="bg-slate-800 p-2 rounded">
                  {t.amount} ALGO –
                  <a
                    className="text-cyan-400 underline ml-2"
                    href={`https://testnet.algoexplorer.io/tx/${t.txId}`}
                    target="_blank"
                  >
                    View on Explorer
                  </a>
                </li>
              ))}
            </ul>
          </div>

        </div>

      </div>

      <ConnectWallet
        openModal={openWalletModal}
        closeModal={() => setOpenWalletModal(false)}
      />
    </div>
  )
}

export default Home
