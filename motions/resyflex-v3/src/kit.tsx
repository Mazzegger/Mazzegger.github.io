import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, Easing, spring, delayRender, continueRender} from 'remotion';

// ================================================================== charte ResyFlex (resy-flex.com)
export const OR = '#f5901e', OR2 = '#ff6a00', GOLD = '#ffc46b', INK = '#11141b', INK2 = '#1b1f2a', CREAM = '#fff7ee', GREEN = '#16a34a', WHITE = '#ffffff';
export const HEAD = 'Poppins, sans-serif', BODY = 'Inter, sans-serif';
export const CX = 510;                       // centre de la zone de sécurité 9:16 (bande droite réservée)
export const FPS = 30;

// ================================================================== polices locales
const fontHandle = delayRender('fonts');
const faces: [string, string, string][] = [
  ['Poppins', '600', 'poppins-latin-600-normal.woff2'], ['Poppins', '700', 'poppins-latin-700-normal.woff2'],
  ['Poppins', '800', 'poppins-latin-800-normal.woff2'], ['Poppins', '900', 'poppins-latin-900-normal.woff2'],
  ['Inter', '400', 'inter-latin-400-normal.woff2'], ['Inter', '500', 'inter-latin-500-normal.woff2'],
  ['Inter', '600', 'inter-latin-600-normal.woff2'], ['Inter', '700', 'inter-latin-700-normal.woff2'],
];
Promise.all(faces.map(([f, w, file]) => new FontFace(f, `url(${staticFile('fonts/' + file)})`, {weight: w}).load().then((ff) => (document as any).fonts.add(ff))))
  .then(() => continueRender(fontHandle)).catch(() => continueRender(fontHandle));

// ================================================================== outils
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const prog = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
export const eOut = (k: number) => Easing.out(Easing.cubic)(clamp(k));
export const eOut5 = (k: number) => Easing.out(Easing.poly(5))(clamp(k));
export const eIn = (k: number) => Easing.in(Easing.cubic)(clamp(k));
export const eInOut = (k: number) => Easing.inOut(Easing.cubic)(clamp(k));
export const eBack = (k: number, s = 1.8) => Easing.out(Easing.back(s))(clamp(k));
export const sp = (t: number, t0: number, d = 12, st = 180) => spring({frame: Math.round((t - t0) * FPS), fps: FPS, config: {damping: d, stiffness: st, mass: 0.8}});
export const useT = () => useCurrentFrame() / FPS;
export const rng = (seed: number) => { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
export const Icon: React.FC<{n: string; s?: number; c?: string; w?: number}> = ({n, s = 48, c = INK, w = 2.2}) => {
  const p: any = {fill: 'none', stroke: c, strokeWidth: w, strokeLinecap: 'round', strokeLinejoin: 'round'};
  const g: Record<string, React.ReactNode> = {
    pin: <><path {...p} d="M12 21s-7-6.5-7-11a7 7 0 0 1 14 0c0 4.5-7 11-7 11z" /><circle {...p} cx="12" cy="10" r="2.5" /></>,
    search: <><circle {...p} cx="11" cy="11" r="7" /><path {...p} d="M16.5 16.5L21 21" /></>,
    nav: <polygon {...p} points="3,11 21,3 13,21 11,13" />,
    sort: <path {...p} d="M7 4v16M3 16l4 4 4-4M17 20V4M13 8l4-4 4 4" />,
    shield: <><path {...p} d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" /><path {...p} d="M8.5 12l2.5 2.5 4.5-5" /></>,
    lock: <><rect {...p} x="5" y="11" width="14" height="10" rx="2" /><path {...p} d="M8 11V8a4 4 0 0 1 8 0v3" /></>,
    refresh: <><path {...p} d="M20 12a8 8 0 1 1-2.4-5.7" /><path {...p} d="M20 4v5h-5" /></>,
    star: <polygon {...p} points="12,3 14.8,9 21,9.6 16.2,13.8 17.6,20 12,16.8 6.4,20 7.8,13.8 3,9.6 9.2,9" />,
    home: <><path {...p} d="M3 11l9-8 9 8" /><path {...p} d="M5 10v10h14V10" /><path {...p} d="M10 20v-6h4v6" /></>,
    phone: <path {...p} d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" />,
    check: <path {...p} d="M5 12.5l4.5 4.5L19 7.5" />,
    wallet: <><rect {...p} x="3" y="6" width="18" height="13" rx="2.5" /><path {...p} d="M3 10h18M16 14.5h2" /></>,
    mobile: <><rect {...p} x="7" y="2.5" width="10" height="19" rx="2.2" /><path {...p} d="M11 18.5h2" /></>,
    bell: <><path {...p} d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z" /><path {...p} d="M10 20a2 2 0 0 0 4 0" /></>,
  };
  return <svg width={s} height={s} viewBox="0 0 24 24">{g[n]}</svg>;
};

export const Kinetic: React.FC<{text: string; t0: number; size: number; color?: string; stroke?: boolean; stagger?: number; weight?: number; style?: React.CSSProperties; spacing?: number}> =
  ({text, t0, size, color = WHITE, stroke = false, stagger = 0.025, weight = 900, style, spacing = -2}) => {
    const t = useT();
    return <div style={{display: 'flex', justifyContent: 'center', fontFamily: HEAD, fontWeight: weight, fontSize: size, lineHeight: 1, letterSpacing: spacing, whiteSpace: 'pre', ...style}}>
      {text.split('').map((ch, i) => {
        const k = prog(t, t0 + i * stagger, t0 + i * stagger + 0.32);
        return <span key={i} style={{display: 'inline-block', overflow: 'hidden', padding: '0.06em 0', margin: '-0.06em 0'}}>
          <span style={{display: 'inline-block', transform: `translateY(${(1 - eOut5(k)) * 105}%) rotate(${(1 - eOut(k)) * 8}deg)`,
            color: stroke ? 'transparent' : color, WebkitTextStroke: stroke ? `3px ${color}` : undefined}}>{ch}</span>
        </span>;
      })}
    </div>;
  };

export const Line: React.FC<{t0: number; children: React.ReactNode; size?: number; color?: string; weight?: number; font?: string; style?: React.CSSProperties}> =
  ({t0, children, size = 44, color = WHITE, weight = 600, font = BODY, style}) => {
    const t = useT(); const k = eOut5(prog(t, t0, t0 + 0.45));
    return <div style={{fontFamily: font, fontWeight: weight, fontSize: size, color, opacity: k, transform: `translateY(${(1 - k) * 36}px)`, filter: `blur(${(1 - k) * 8}px)`, ...style}}>{children}</div>;
  };

export const Box: React.FC<{y: number; w?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({y, w = 900, children, style}) =>
  <div style={{position: 'absolute', left: CX - w / 2, top: y, width: w, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', ...style}}>{children}</div>;

export const DarkBG: React.FC<{hue?: string}> = ({hue = OR}) => {
  const t = useT();
  return <AbsoluteFill style={{background: INK, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: -300 + 120 * Math.sin(t * 0.5), top: 200 + 80 * Math.cos(t * 0.4), width: 1400, height: 1400, borderRadius: '50%',
      background: `radial-gradient(circle, ${hue}55 0%, transparent 60%)`}} />
    <div style={{position: 'absolute', left: 300 + 100 * Math.cos(t * 0.35), top: 1000 + 90 * Math.sin(t * 0.45), width: 1300, height: 1300, borderRadius: '50%',
      background: `radial-gradient(circle, ${OR2}33 0%, transparent 60%)`}} />
    {/* grille fine en perspective */}
    <div style={{position: 'absolute', left: -200, right: -200, bottom: -100, height: 900, transform: 'perspective(700px) rotateX(62deg)', transformOrigin: 'bottom',
      backgroundImage: `linear-gradient(${OR}22 2px, transparent 2px), linear-gradient(90deg, ${OR}22 2px, transparent 2px)`, backgroundSize: '90px 90px',
      backgroundPosition: `0 ${(t * 120) % 90}px`, maskImage: 'linear-gradient(to top, black, transparent)', WebkitMaskImage: 'linear-gradient(to top, black, transparent)'}} />
  </AbsoluteFill>;
};

export const CreamBG: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: CREAM, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: -200 + 60 * Math.sin(t), top: 100, width: 1200, height: 1200, borderRadius: '50%', background: `radial-gradient(circle, ${OR}40 0%, transparent 62%)`}} />
    <div style={{position: 'absolute', left: 300, top: 1100 + 60 * Math.cos(t), width: 1200, height: 1200, borderRadius: '50%', background: `radial-gradient(circle, ${GOLD}55 0%, transparent 62%)`}} />
  </AbsoluteFill>;
};

// photo plein cadre avec Ken Burns

export const KenBurns: React.FC<{src: string; t0: number; dur?: number; from?: number; to?: number; dx?: number; style?: React.CSSProperties}> = ({src, t0, dur = 2, from = 1.25, to = 1.05, dx = 0, style}) => {
  const t = useT(); const k = prog(t, t0, t0 + dur);
  return <AbsoluteFill style={{overflow: 'hidden', ...style}}>
    <Img src={staticFile(`img/${src}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${from + (to - from) * eOut(k)}) translateX(${dx * k}px)`}} />
  </AbsoluteFill>;
};

export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.22}}>
    <svg width="1080" height="1920"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={f % 30} /><feColorMatrix type="saturate" values="0" /></filter>
      <rect width="1080" height="1920" filter="url(#g)" /></svg>
  </AbsoluteFill>;
};

export const Flare: React.FC<{t0: number; y?: number}> = ({t0, y = 960}) => {
  const t = useT(); const k = prog(t, t0, t0 + 0.6); if (k <= 0 || k >= 1) return null;
  return <div style={{position: 'absolute', left: -200, width: 1480, top: y - 6, height: 12, borderRadius: 12, mixBlendMode: 'screen',
    background: `linear-gradient(90deg, transparent, rgba(255,190,90,${0.9 * (1 - k)}), rgba(255,255,255,${1 - k}), rgba(255,190,90,${0.9 * (1 - k)}), transparent)`,
    transform: `scaleX(${0.3 + 0.9 * eOut(k)}) scaleY(${1 + 3 * (1 - k)})`, filter: 'blur(2px)'}} />;
};

export const Flash: React.FC<{t0: number; d?: number; a?: number; c?: string}> = ({t0, d = 0.25, a = 0.9, c = WHITE}) => {
  const t = useT(); const k = prog(t, t0, t0 + d); if (k <= 0 || k >= 1) return null;
  return <AbsoluteFill style={{background: c, opacity: a * (1 - eOut(k))}} />;
};

export const Ring: React.FC<{t0: number; x?: number; y: number; r?: number; c?: string; w?: number}> = ({t0, x = CX, y, r = 700, c = OR, w = 16}) => {
  const t = useT(); const k = prog(t, t0, t0 + 0.7); if (k <= 0 || k >= 1) return null; const rr = r * eOut(k);
  return <div style={{position: 'absolute', left: x - rr, top: y - rr, width: 2 * rr, height: 2 * rr, borderRadius: '50%', border: `${w * (1 - k) + 1}px solid ${c}`, opacity: 1 - k}} />;
};

export const Particles: React.FC<{t0: number; x?: number; y: number; n?: number; colors?: string[]; dist?: number; seed?: number}> = ({t0, x = CX, y, n = 40, colors = [OR, GOLD, WHITE], dist = 520, seed = 3}) => {
  const t = useT(); const k = prog(t, t0, t0 + 1.1); if (k <= 0 || k >= 1) return null; const r = rng(seed);
  return <>{Array.from({length: n}).map((_, i) => {
    const a = r() * Math.PI * 2, d = dist * (0.35 + r() * 0.8) * eOut(k), s = 6 + r() * 14;
    return <div key={i} style={{position: 'absolute', left: x + Math.cos(a) * d, top: y + Math.sin(a) * d + 260 * k * k, width: s, height: s, borderRadius: i % 3 ? '50%' : 3,
      background: colors[i % colors.length], opacity: 1 - k, transform: `rotate(${k * 400 * (r() - 0.5)}deg)`}} />;
  })}</>;
};

export const Phone3D: React.FC<{x: number; y: number; w: number; ry?: number; rx?: number; rz?: number; scale?: number; children: React.ReactNode}> = ({x, y, w, ry = 0, rx = 0, rz = 0, scale = 1, children}) => {
  const h = w * 2.16;
  return <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, perspective: 2200}}>
    <div style={{width: '100%', height: '100%', transformStyle: 'preserve-3d', transform: `scale(${scale}) rotateY(${ry}deg) rotateX(${rx}deg) rotateZ(${rz}deg)`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: w * 0.13, background: 'linear-gradient(145deg,#2a2f3a,#0b0d12)', padding: w * 0.03,
        boxShadow: `${-ry * 2}px 60px 120px rgba(0,0,0,0.55), inset 0 0 0 3px #3a404d`}}>
        <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: w * 0.105, overflow: 'hidden', background: '#f7f8fa'}}>
          {children}
          <div style={{position: 'absolute', top: w * 0.025, left: '50%', transform: 'translateX(-50%)', width: w * 0.3, height: w * 0.075, borderRadius: 40, background: '#0b0d12'}} />
          <div style={{position: 'absolute', inset: 0, background: `linear-gradient(${110 + ry * 2}deg, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0) 35%)`, mixBlendMode: 'screen'}} />
        </div>
      </div>
    </div>
  </div>;
};

export const Screen: React.FC<{src: string; scroll?: number; opacity?: number}> = ({src, scroll = 0, opacity = 1}) =>
  <Img src={staticFile(`ui/${src}.png`)} style={{position: 'absolute', left: 0, top: 0, width: '100%', transform: `translateY(${-scroll}%)`, opacity}} />;
export const LightLeaks: React.FC<{hits: [number, number][]}> = ({hits}) => {
  const t = useT();
  const boost = hits.reduce((a, [h, amp]) => a + (t >= h ? Math.exp(-(t - h) * 5) * amp / 30 : 0), 0);
  return <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen'}}>
    <div style={{position: 'absolute', left: 700 + 200 * Math.sin(t * 0.7), top: -300 + 150 * Math.cos(t * 0.5), width: 900, height: 900, borderRadius: '50%',
      background: `radial-gradient(circle, rgba(255,170,60,${0.18 + 0.35 * clamp(boost)}) 0%, transparent 65%)`, filter: 'blur(20px)'}} />
    <div style={{position: 'absolute', left: -400 + 150 * Math.cos(t * 0.6), top: 1300 + 120 * Math.sin(t * 0.8), width: 1000, height: 1000, borderRadius: '50%',
      background: `radial-gradient(circle, rgba(255,110,20,${0.12 + 0.3 * clamp(boost)}) 0%, transparent 65%)`, filter: 'blur(30px)'}} />
  </AbsoluteFill>;
};

// reflet anamorphique horizontal sur les impacts
export const QR: React.FC<{t: number; build: [number, number]}> = ({t, build}) => {
  const N = 21; const r = rng(17); const cells: React.ReactNode[] = [];
  const finder = (y: number, x: number) => { for (const [fy, fx] of [[0, 0], [0, N - 7], [N - 7, 0]]) { const a = y - fy, b = x - fx; if (a >= 0 && a < 7 && b >= 0 && b < 7) return (a === 0 || a === 6 || b === 0 || b === 6 || (a >= 2 && a <= 4 && b >= 2 && b <= 4)) ? 1 : 0; } return -1; };
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const f = finder(y, x); const v = f === -1 ? r() > 0.5 : f === 1; const ap = build[0] + r() * (build[1] - build[0]); if (!v) continue;
    const k = eBack(prog(t, ap, ap + 0.15)); cells.push(<rect key={y * N + x} x={x * 14 + 7 * (1 - k)} y={y * 14 + 7 * (1 - k)} width={14 * k} height={14 * k} rx={2} fill={INK} />);
  }
  return <svg width={294} height={294} viewBox="0 0 294 294">{cells}</svg>;
};
