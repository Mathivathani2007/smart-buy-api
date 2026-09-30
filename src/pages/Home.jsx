import { useRef, useState } from 'react'
import { ArrowRight, BrainCircuit, Camera, CheckCircle2, CloudUpload, Search, ShieldCheck, Sparkles, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const MAX_SIZE = 8 * 1024 * 1024
const accepted = ['image/jpeg', 'image/png', 'image/webp']

export default function Home() {
  const navigate = useNavigate()
  const inputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState('')
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [dragging, setDragging] = useState(false)

  function chooseImage(nextFile) {
    setError('')
    if (!nextFile) return
    if (!accepted.includes(nextFile.type)) return setError('Please upload a JPG, PNG or WEBP image.')
    if (!nextFile.size || nextFile.size > MAX_SIZE) return setError('The image is too large. Please choose an image under 8 MB.')
    setFile(nextFile)
    const reader = new FileReader()
    reader.onload = () => setPreview(reader.result)
    reader.readAsDataURL(nextFile)
    if (inputRef.current) inputRef.current.value = ''
  }
  function analyze() { if (file) navigate('/results', { state: { file, preview } }) }
  function search() { if (query.trim()) navigate('/results', { state: { query: query.trim() } }) }

  return <main>
    <nav className="nav shell"><a className="brand" href="/"><span className="brand-mark"><Sparkles size={17} /></span><span>SMARTBUY <em>AI</em></span></a><div className="nav-links"><a href="#how">How it works</a><a href="#features">Features</a><a href="#about">About</a></div><button className="nav-cta" onClick={() => inputRef.current?.click()}>Upload product <ArrowRight size={16} /></button></nav>
    <section className="hero shell"><div className="hero-copy"><div className="eyebrow"><span className="pulse-dot" /> AI-POWERED PRODUCT INTELLIGENCE</div><h1>Don't just compare prices.<br /><span>Find the smartest choice.</span></h1><p>Upload a product image and SmartBuy AI compares price, ratings and review insights across India's top marketplaces.</p><div className="trust-row"><span><CheckCircle2 size={16} /> Four marketplaces</span><span><ShieldCheck size={16} /> Demo-ready & private</span></div></div><div className="upload-panel" id="upload"><div className="panel-top"><div><span className="panel-kicker">START HERE</span><h2>What are you shopping for?</h2></div><Camera size={24} className="panel-icon" /></div><div className={`dropzone ${dragging ? 'dragging' : ''} ${preview ? 'has-preview' : ''}`} onDragOver={(e) => { e.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={(e) => { e.preventDefault(); setDragging(false); chooseImage(e.dataTransfer.files[0]) }} onClick={() => !preview && inputRef.current?.click()} role="button" tabIndex="0" onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}>
      {preview ? <><img src={preview} alt="Selected product preview" /><button className="remove" onClick={(e) => { e.stopPropagation(); setFile(null); setPreview(''); if (inputRef.current) inputRef.current.value = '' }} aria-label="Remove image"><X size={18} /></button><div className="preview-label">Ready to analyze <CheckCircle2 size={16} /></div></> : <><div className="upload-icon"><CloudUpload size={27} /></div><strong>Drop a product image here</strong><span>or click to browse your device</span><small>JPG, PNG or WEBP · up to 8 MB</small></>}
    </div><input ref={inputRef} type="file" hidden accept="image/jpeg,image/png,image/webp" onChange={(e) => chooseImage(e.target.files[0])} />{error && <p className="form-error">{error}</p>}<button className="primary full" disabled={!file} onClick={analyze}>Analyze product <ArrowRight size={18} /></button><div className="divider"><span>or search manually</span></div><div className="search-row"><Search size={18} /><input value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && search()} placeholder="e.g. wireless headphones" aria-label="Search product name" /><button onClick={search} aria-label="Search"><ArrowRight size={18} /></button></div></div></section>
    <section className="market-strip shell"><span>COMPARE ACROSS</span><b>amazon</b><b>flipkart</b><b>meesho</b><b>myntra</b></section>
    <section className="how shell" id="how"><div className="section-label">THE SMARTER WAY TO SHOP</div><h2>From photo to confident decision.</h2><div className="steps"><Step number="01" icon={<Camera />} title="Show us the product" text="Upload a photo or search what you have in mind." /><Step number="02" icon={<BrainCircuit />} title="We do the research" text="We identify it, match listings and read the signals in reviews." /><Step number="03" icon={<Sparkles />} title="You choose better" text="One transparent score makes the best value easy to spot." /></div></section>
    <footer className="footer shell" id="about"><span className="brand"><span className="brand-mark"><Sparkles size={15} /></span>SMARTBUY <em>AI</em></span><span>Marketplace data shown in demo mode · Built for smarter decisions.</span></footer>
  </main>
}
function Step({ number, icon, title, text }) { return <div className="step"><span className="step-number">{number}</span><div className="step-icon">{icon}</div><h3>{title}</h3><p>{text}</p></div> }
