import { motion, useScroll, useSpring } from 'framer-motion';
import Navbar      from './components/Navbar';
import Hero        from './components/Hero';
import Marquee     from './components/Marquee';
import Features    from './components/Features';
import HowItWorks  from './components/HowItWorks';
import Stats       from './components/Stats';
import CtaFooter   from './components/CtaFooter';

export default function App() {
  const { scrollYProgress } = useScroll();
  const progress = useSpring(scrollYProgress, { stiffness: 120, damping: 26, restDelta: 0.001 });

  return (
    <div className="relative min-h-screen bg-ink-950 font-inter text-white">
      {/* Reading progress */}
      <motion.div
        style={{ scaleX: progress }}
        className="fixed inset-x-0 top-0 z-[70] h-[2px] origin-left bg-gradient-to-r from-gold-300 via-gold-400 to-gold-600"
      />

      {/* Film grain over everything */}
      <div className="grain" aria-hidden="true" />

      <Navbar />
      <main>
        <Hero />
        <Marquee />
        <Features />
        <HowItWorks />
        <Stats />
        <CtaFooter />
      </main>
    </div>
  );
}
