import Navbar    from './components/Navbar';
import Hero       from './components/Hero';
import Features   from './components/Features';
import HowItWorks from './components/HowItWorks';
import Stats      from './components/Stats';
import CtaFooter  from './components/CtaFooter';

export default function App() {
  return (
    <div className="font-inter bg-[#0a0f1e] text-white">
      <Navbar />
      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <Stats />
        <CtaFooter />
      </main>
    </div>
  );
}
