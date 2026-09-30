import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Results from './pages/Results'

export default function App() {
  function handleImageError(event) {
    const image = event.target
    if (image instanceof HTMLImageElement && image.dataset.fallback !== 'true') {
      image.dataset.fallback = 'true'
      const label = image.alt || 'Product image unavailable'
      image.src = `data:image/svg+xml,${encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480"><rect width="640" height="480" fill="#e8efe3"/><text x="320" y="220" text-anchor="middle" font-family="sans-serif" font-size="34" font-weight="700" fill="#557050">' + label.slice(0, 28) + '</text><text x="320" y="270" text-anchor="middle" font-family="sans-serif" font-size="18" fill="#71806d">Image unavailable</text></svg>')}`
    }
  }

  return <div onError={handleImageError}><Routes><Route path="/" element={<Home />} /><Route path="/results" element={<Results />} /><Route path="*" element={<Home />} /></Routes></div>
}
