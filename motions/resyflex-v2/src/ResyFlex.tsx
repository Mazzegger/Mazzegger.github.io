import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, Easing, spring, delayRender, continueRender} from 'remotion';
import TL from './timeline.json';
import MAP from './civ_map.json';

// ================================================================== charte ResyFlex (resy-flex.com)
const OR = '#f5901e', OR2 = '#ff6a00', GOLD = '#ffc46b', INK = '#11141b', INK2 = '#1b1f2a', CREAM = '#fff7ee', GREEN = '#16a34a', WHITE = '#ffffff';
const HEAD = 'Poppins, sans-serif', BODY = 'Inter, sans-serif';
const CX = 510;                       // centre de la zone de sécurité 9:16 (bande droite réservée)
const E: any = TL.ev, SC: any = TL.scenes, FPS = TL.fps;

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
const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
const eOut = (k: number) => Easing.out(Easing.cubic)(clamp(k));
const eOut5 = (k: number) => Easing.out(Easing.poly(5))(clamp(k));
const eIn = (k: number) => Easing.in(Easing.cubic)(clamp(k));
const eInOut = (k: number) => Easing.inOut(Easing.cubic)(clamp(k));
const eBack = (k: number, s = 1.8) => Easing.out(Easing.back(s))(clamp(k));
const sp = (t: number, t0: number, d = 12, st = 180) => spring({frame: Math.round((t - t0) * FPS), fps: FPS, config: {damping: d, stiffness: st, mass: 0.8}});
const useT = () => useCurrentFrame() / FPS;
const on = (t: number, k: string, pre = 0, post = 0) => t >= SC[k][0] - pre && t < SC[k][1] + post;
const rng = (seed: number) => { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
// impacts (secousse caméra) : instant, amplitude
const HITS: [number, number][] = [[E.drop, 34], [E.words[0], 10], [E.words[1], 10], [E.words[2], 14], [E.cities, 12], [E.stamp, 26], [E.ten, 30], [E.min, 10],
  [E.thirty, 24], [E.scanOk, 12], ...E.trust.map((x: number) => [x, 9] as [number, number]), [E.ctaHit, 36]];

// ================================================================== icônes
const Icon: React.FC<{n: string; s?: number; c?: string; w?: number}> = ({n, s = 48, c = INK, w = 2.2}) => {
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

// ================================================================== typographie cinétique
// mot géant, lettres qui surgissent d'un masque, décalées
const Kinetic: React.FC<{text: string; t0: number; size: number; color?: string; stroke?: boolean; stagger?: number; weight?: number; style?: React.CSSProperties; spacing?: number}> =
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

const Line: React.FC<{t0: number; children: React.ReactNode; size?: number; color?: string; weight?: number; font?: string; style?: React.CSSProperties}> =
  ({t0, children, size = 44, color = WHITE, weight = 600, font = BODY, style}) => {
    const t = useT(); const k = eOut5(prog(t, t0, t0 + 0.45));
    return <div style={{fontFamily: font, fontWeight: weight, fontSize: size, color, opacity: k, transform: `translateY(${(1 - k) * 36}px)`, filter: `blur(${(1 - k) * 8}px)`, ...style}}>{children}</div>;
  };

const Box: React.FC<{y: number; w?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({y, w = 900, children, style}) =>
  <div style={{position: 'absolute', left: CX - w / 2, top: y, width: w, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', ...style}}>{children}</div>;

// ================================================================== fonds et effets
const DarkBG: React.FC<{hue?: string}> = ({hue = OR}) => {
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

const CreamBG: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: CREAM, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: -200 + 60 * Math.sin(t), top: 100, width: 1200, height: 1200, borderRadius: '50%', background: `radial-gradient(circle, ${OR}40 0%, transparent 62%)`}} />
    <div style={{position: 'absolute', left: 300, top: 1100 + 60 * Math.cos(t), width: 1200, height: 1200, borderRadius: '50%', background: `radial-gradient(circle, ${GOLD}55 0%, transparent 62%)`}} />
  </AbsoluteFill>;
};

// photo plein cadre avec Ken Burns
const KenBurns: React.FC<{src: string; t0: number; dur?: number; from?: number; to?: number; dx?: number; style?: React.CSSProperties}> = ({src, t0, dur = 2, from = 1.25, to = 1.05, dx = 0, style}) => {
  const t = useT(); const k = prog(t, t0, t0 + dur);
  return <AbsoluteFill style={{overflow: 'hidden', ...style}}>
    <Img src={staticFile(`img/${src}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${from + (to - from) * eOut(k)}) translateX(${dx * k}px)`}} />
  </AbsoluteFill>;
};

const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.22}}>
    <svg width="1080" height="1920"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={f % 30} /><feColorMatrix type="saturate" values="0" /></filter>
      <rect width="1080" height="1920" filter="url(#g)" /></svg>
  </AbsoluteFill>;
};

const LightLeaks: React.FC = () => {
  const t = useT();
  const boost = HITS.reduce((a, [h, amp]) => a + (t >= h ? Math.exp(-(t - h) * 5) * amp / 30 : 0), 0);
  return <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'screen'}}>
    <div style={{position: 'absolute', left: 700 + 200 * Math.sin(t * 0.7), top: -300 + 150 * Math.cos(t * 0.5), width: 900, height: 900, borderRadius: '50%',
      background: `radial-gradient(circle, rgba(255,170,60,${0.18 + 0.35 * clamp(boost)}) 0%, transparent 65%)`, filter: 'blur(20px)'}} />
    <div style={{position: 'absolute', left: -400 + 150 * Math.cos(t * 0.6), top: 1300 + 120 * Math.sin(t * 0.8), width: 1000, height: 1000, borderRadius: '50%',
      background: `radial-gradient(circle, rgba(255,110,20,${0.12 + 0.3 * clamp(boost)}) 0%, transparent 65%)`, filter: 'blur(30px)'}} />
  </AbsoluteFill>;
};

// reflet anamorphique horizontal sur les impacts
const Flare: React.FC<{t0: number; y?: number}> = ({t0, y = 960}) => {
  const t = useT(); const k = prog(t, t0, t0 + 0.6); if (k <= 0 || k >= 1) return null;
  return <div style={{position: 'absolute', left: -200, width: 1480, top: y - 6, height: 12, borderRadius: 12, mixBlendMode: 'screen',
    background: `linear-gradient(90deg, transparent, rgba(255,190,90,${0.9 * (1 - k)}), rgba(255,255,255,${1 - k}), rgba(255,190,90,${0.9 * (1 - k)}), transparent)`,
    transform: `scaleX(${0.3 + 0.9 * eOut(k)}) scaleY(${1 + 3 * (1 - k)})`, filter: 'blur(2px)'}} />;
};
const Flash: React.FC<{t0: number; d?: number; a?: number; c?: string}> = ({t0, d = 0.25, a = 0.9, c = WHITE}) => {
  const t = useT(); const k = prog(t, t0, t0 + d); if (k <= 0 || k >= 1) return null;
  return <AbsoluteFill style={{background: c, opacity: a * (1 - eOut(k))}} />;
};
const Ring: React.FC<{t0: number; x?: number; y: number; r?: number; c?: string; w?: number}> = ({t0, x = CX, y, r = 700, c = OR, w = 16}) => {
  const t = useT(); const k = prog(t, t0, t0 + 0.7); if (k <= 0 || k >= 1) return null; const rr = r * eOut(k);
  return <div style={{position: 'absolute', left: x - rr, top: y - rr, width: 2 * rr, height: 2 * rr, borderRadius: '50%', border: `${w * (1 - k) + 1}px solid ${c}`, opacity: 1 - k}} />;
};
const Particles: React.FC<{t0: number; x?: number; y: number; n?: number; colors?: string[]; dist?: number; seed?: number}> = ({t0, x = CX, y, n = 40, colors = [OR, GOLD, WHITE], dist = 520, seed = 3}) => {
  const t = useT(); const k = prog(t, t0, t0 + 1.1); if (k <= 0 || k >= 1) return null; const r = rng(seed);
  return <>{Array.from({length: n}).map((_, i) => {
    const a = r() * Math.PI * 2, d = dist * (0.35 + r() * 0.8) * eOut(k), s = 6 + r() * 14;
    return <div key={i} style={{position: 'absolute', left: x + Math.cos(a) * d, top: y + Math.sin(a) * d + 260 * k * k, width: s, height: s, borderRadius: i % 3 ? '50%' : 3,
      background: colors[i % colors.length], opacity: 1 - k, transform: `rotate(${k * 400 * (r() - 0.5)}deg)`}} />;
  })}</>;
};

// ================================================================== téléphone 3D avec la vraie interface
const Phone3D: React.FC<{x: number; y: number; w: number; ry?: number; rx?: number; rz?: number; scale?: number; children: React.ReactNode}> = ({x, y, w, ry = 0, rx = 0, rz = 0, scale = 1, children}) => {
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
const Screen: React.FC<{src: string; scroll?: number; opacity?: number}> = ({src, scroll = 0, opacity = 1}) =>
  <Img src={staticFile(`ui/${src}.png`)} style={{position: 'absolute', left: 0, top: 0, width: '100%', transform: `translateY(${-scroll}%)`, opacity}} />;

// ================================================================== caméra : pulsation sur la grosse caisse + secousses
const Camera: React.FC<{children: React.ReactNode}> = ({children}) => {
  const t = useT();
  let shake = 0; for (const [h, amp] of HITS) if (t >= h) shake += amp * Math.exp(-(t - h) * 9);
  const r = rng(Math.floor(t * 60) + 11);
  const beat = t >= E.drop && t < E.fade ? ((t - E.drop) % 0.5) : 9;          // grosse caisse sur chaque temps après le drop
  const cut = t >= TL.music.cut[0] && t < TL.music.cut[1];
  const pulse = cut ? 0 : 0.018 * Math.exp(-beat * 10);
  return <AbsoluteFill style={{transform: `translate(${(r() - 0.5) * shake}px, ${(r() - 0.5) * shake}px) scale(${1 + pulse}) rotate(${(r() - 0.5) * shake * 0.03}deg)`}}>{children}</AbsoluteFill>;
};

// ================================================================== 1. accroche : villes + phrase
const CITY_CUTS = [['abidjan', 'ABIDJAN'], ['korhogo', 'KORHOGO'], ['sanpedro', 'SAN-PEDRO'], ['grandlahou', 'GRAND-LAHOU']];
const Hook: React.FC = () => {
  const t = useT(); if (!on(t, 'hook')) return null;
  const ci = E.cityCuts.filter((x: number) => t >= x).length - 1;
  const inCities = t < E.hookLine[0];
  const holeK = 0; // (le trou en forme de logo est dans la scène suivante)
  return <AbsoluteFill style={{background: '#000'}}>
    {inCities && ci >= 0 && <>
      <KenBurns src={CITY_CUTS[ci][0]} t0={E.cityCuts[ci]} dur={0.6} from={1.35} to={1.12} dx={ci % 2 ? -40 : 40} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.1) 40%, rgba(0,0,0,0.65) 100%)'}} />
      <Box y={840}><Kinetic text={CITY_CUTS[ci][1]} t0={E.cityCuts[ci]} size={CITY_CUTS[ci][1].length > 9 ? 100 : CITY_CUTS[ci][1].length > 7 ? 116 : 140} stagger={0.018} /></Box>
      <Box y={1000}><Line t0={E.cityCuts[ci] + 0.08} size={44} color={GOLD} weight={700}>Résidences meublées</Line></Box>
      <Flash t0={E.cityCuts[ci]} d={0.12} a={0.55} />
    </>}
    {!inCities && <>
      <DarkBG />
      <AbsoluteFill style={{transform: `scale(${1 + 0.25 * eIn(prog(t, 2.0, 4.0))})`}}>
        <Box y={700}><Kinetic text="Votre résidence" t0={E.hookLine[0]} size={100} stagger={0.02} /></Box>
        <Box y={820}><Kinetic text="meublée," t0={E.hookLine[0] + 0.2} size={100} stagger={0.02} /></Box>
        <Box y={990}><Kinetic text="partout en" t0={E.hookLine[1]} size={78} color={GOLD} weight={800} stagger={0.02} /></Box>
        <Box y={1080}><Kinetic text="Côte d’Ivoire" t0={E.hookLine[1] + 0.15} size={118} color={OR} stagger={0.025} /></Box>
      </AbsoluteFill>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${CX}px 960px, transparent ${(1 - prog(t, 3.0, 4.0)) * 1400}px, rgba(0,0,0,0.85) ${(1 - prog(t, 3.0, 4.0)) * 1400 + 300}px)`}} />
    </>}
    <Flash t0={E.whiteout} d={0.25} a={0} />
    <AbsoluteFill style={{background: WHITE, opacity: prog(t, E.whiteout, E.drop) * 0.9}} />
  </AbsoluteFill>;
};

// ================================================================== 2. drop : le logo s'ouvre en forme de symbole ResyFlex
const Logo: React.FC = () => {
  const t = useT(); if (!on(t, 'logo')) return null;
  const mk = eIn(prog(t, E.drop, E.drop + 0.55));            // le symbole grossit jusqu'à envahir l'écran
  const s = sp(t, E.drop + 0.15, 10, 160);
  const out = eIn(prog(t, E.zoomThrough, SC.logo[1]));       // zoom traversant vers la scène suivante
  const words = [['TROUVEZ', OR], ['RÉSERVEZ', INK], ['SÉJOURNEZ', OR]];
  return <AbsoluteFill style={{transform: `scale(${1 + out * 3.5})`, filter: `blur(${out * 18}px)`, opacity: 1 - prog(t, SC.logo[1] - 0.1, SC.logo[1])}}>
    <AbsoluteFill style={{background: '#000'}} />
    {/* scène crème révélée à travers la forme du symbole du logo */}
    <AbsoluteFill style={{WebkitMaskImage: `url(${staticFile('img/logo-mark.png')})`, maskImage: `url(${staticFile('img/logo-mark.png')})`,
      WebkitMaskRepeat: 'no-repeat', maskRepeat: 'no-repeat', WebkitMaskPosition: `${CX - 270 * (0.4 + mk * 30)}px ${960 - 165 * (0.4 + mk * 30)}px`,
      maskPosition: `${CX - 270 * (0.4 + mk * 30)}px ${960 - 165 * (0.4 + mk * 30)}px`, WebkitMaskSize: `${540 * (0.4 + mk * 30)}px auto`, maskSize: `${540 * (0.4 + mk * 30)}px auto`}}>
      <CreamBG />
      <Ring t0={E.drop + 0.25} y={760} r={900} />
      <Ring t0={E.drop + 0.33} y={760} r={650} c={GOLD} w={10} />
      <div style={{position: 'absolute', left: CX - 440, top: 620, width: 880, transform: `scale(${0.4 + 0.6 * s}) rotate(${(1 - s) * -6}deg)`}}>
        <Img src={staticFile('img/logo-full.png')} style={{width: 880}} />
      </div>
      {words.map(([w, c], i) => {
        const t0 = E.words[i]; const k = eOut5(prog(t, t0, t0 + 0.3));
        return <div key={w} style={{position: 'absolute', left: 0, width: 1020, top: 960 + i * 150, display: 'flex', justifyContent: 'center'}}>
          <div style={{transform: `translateX(${(1 - k) * (i % 2 ? 900 : -900)}px) skewX(${(1 - k) * -20}deg)`, fontFamily: HEAD, fontWeight: 900, fontSize: 132, color: c as string, letterSpacing: -3}}>{w}</div>
        </div>;
      })}
      <Particles t0={E.drop + 0.2} y={760} n={46} dist={700} />
    </AbsoluteFill>
    <Flash t0={E.drop} d={0.2} a={0.85} />
    <Flare t0={E.drop + 0.05} y={760} />
  </AbsoluteFill>;
};

// ================================================================== 3. trouvez : vraie interface dans un téléphone 3D
const CALLOUTS: [string, string, number, number][] = [['search', 'Recherche par ville', -1, 620], ['nav', 'Autour de moi', 1, 820], ['sort', 'Tri par prix', -1, 1020], ['shield', 'Logements vérifiés', 1, 1220]];
const Find: React.FC = () => {
  const t = useT(); if (!on(t, 'find', 0, 0.25)) return null;
  const inK = eOut5(prog(t, SC.find[0], SC.find[0] + 0.7));
  const whip = eIn(prog(t, E.whip, E.whip + 0.25));
  const ry = -38 * (1 - inK) + 10 * Math.sin((t - 8) * 0.9) * inK, rx = 14 * (1 - inK);
  const scroll = 52 * eInOut(prog(t, E.listIn + 0.3, E.whip));
  return <AbsoluteFill style={{transform: `translateX(${-whip * 1300}px)`, filter: `blur(${whip * 24}px)`}}>
    <DarkBG />
    <div style={{position: 'absolute', left: -60, top: 1520, width: 1200, transform: `translateX(${-(t - 8) * 60}px)`, opacity: 0.9}}>
      <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 240, color: 'transparent', WebkitTextStroke: `3px ${OR}66`, whiteSpace: 'nowrap', letterSpacing: -4}}>TROUVEZ TROUVEZ</div>
    </div>
    <Box y={250}><Kinetic text="01 · TROUVEZ" t0={SC.find[0] + 0.15} size={72} color={WHITE} stagger={0.02} /></Box>
    <Phone3D x={CX} y={1040 + (1 - inK) * 600} w={470} ry={ry} rx={rx}>
      <Screen src="home" opacity={1 - prog(t, E.listIn, E.listIn + 0.2)} />
      {t >= E.listIn && <div style={{position: 'absolute', inset: 0, overflow: 'hidden', transform: `translateX(${(1 - eOut5(prog(t, E.listIn, E.listIn + 0.35))) * 100}%)`}}>
        <Img src={staticFile('ui/list.png')} style={{position: 'absolute', left: 0, top: 0, width: '100%', transform: `translateY(${-scroll * 0.08 * 10}%)`}} />
      </div>}
    </Phone3D>
    {CALLOUTS.map(([ic, lab, side, y], i) => {
      const t0 = E.callouts[i]; const k = eBack(prog(t, t0, t0 + 0.35), 2.2); if (t < t0) return null;
      const x = side < 0 ? 40 : 520;
      return <div key={lab} style={{position: 'absolute', left: x, top: y, transform: `scale(${k})`, transformOrigin: side < 0 ? 'right center' : 'left center', opacity: clamp(k * 2),
        display: 'flex', alignItems: 'center', gap: 14, padding: '18px 26px', borderRadius: 50, background: 'rgba(255,255,255,0.96)', boxShadow: '0 18px 40px rgba(0,0,0,0.35)'}}>
        <div style={{width: 58, height: 58, borderRadius: 29, background: OR, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon n={ic} s={34} c={WHITE} w={2.6} /></div>
        <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 36, color: INK}}>{lab}</span>
      </div>;
    })}
  </AbsoluteFill>;
};

// ================================================================== 4. carte de Côte d'Ivoire
const LABEL: Record<string, [number, number, string]> = {
  'Abidjan': [-24, -46, 'end'], 'Bingerville': [26, -40, 'start'], 'Grand-Bassam': [24, 44, 'start'], 'San-Pedro': [0, 52, 'middle'],
  'Korhogo': [26, -16, 'start'], 'Boundiali': [-24, -16, 'end'], 'Grand-Lahou': [0, 52, 'middle'],
};
const PIN_ORDER = ['Abidjan', 'San-Pedro', 'Korhogo', 'Grand-Bassam', 'Bingerville', 'Boundiali', 'Grand-Lahou'];
const MapScene: React.FC = () => {
  const t = useT(); if (!on(t, 'map', 0.25, 0.25)) return null;
  const inK = eOut5(prog(t, SC.map[0] - 0.25, SC.map[0] + 0.2));
  const draw = eInOut(prog(t, E.mapDraw, E.mapDraw + 1.0));
  const out = eIn(prog(t, E.toVerify, SC.map[1] + 0.2));
  const S = 0.9, ox = CX - MAP.w * S / 2, oy = 470;
  const cnt = PIN_ORDER.filter((_, i) => t >= E.pins[i]).length;
  return <AbsoluteFill style={{transform: `translateX(${(1 - inK) * 1300 - out * 0}px) scale(${1 + out * 0.4})`, filter: `blur(${(1 - inK) * 20 + out * 16}px)`, opacity: 1 - out}}>
    <DarkBG hue={GOLD} />
    <Box y={210} style={{opacity: cnt > 0 ? 1 : 0}}>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 22}}>
        <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 210, color: OR, lineHeight: 1, transform: `scale(${t >= E.cities ? 1 + 0.25 * Math.exp(-(t - E.cities) * 9) : 1})`}}>{cnt}</div>
        <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 96, color: WHITE, lineHeight: 1}}>{cnt > 1 ? 'villes' : 'ville'}</div>
      </div>
      <Line t0={E.cities} size={44} color={GOLD} weight={700} style={{marginTop: 6}}>déjà disponibles</Line>
    </Box>
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      <defs><linearGradient id="civ" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor={OR} stopOpacity="0.35" /><stop offset="1" stopColor={OR2} stopOpacity="0.15" /></linearGradient></defs>
      <g transform={`translate(${ox} ${oy}) scale(${S})`}>
        <path d={MAP.d} fill="url(#civ)" fillOpacity={eOut(prog(t, E.mapDraw + 0.6, E.mapDraw + 1.2))} stroke={OR} strokeWidth={4 / S} strokeLinejoin="round"
          strokeDasharray={MAP.len} strokeDashoffset={MAP.len * (1 - draw)} style={{filter: 'drop-shadow(0 0 12px rgba(245,144,30,0.6))'}} />
        {PIN_ORDER.map((c, i) => {
          const [x, y] = (MAP.cities as any)[c]; const t0 = E.pins[i]; if (t < t0) return null;
          const k = eBack(prog(t, t0, t0 + 0.3), 2.5); const rip = prog(t, t0, t0 + 0.9); const [lx, ly, an] = LABEL[c];
          return <g key={c}>
            <circle cx={x} cy={y} r={(14 + 60 * eOut(rip)) / S} fill="none" stroke={GOLD} strokeWidth={4 / S} opacity={1 - rip} />
            <circle cx={x} cy={y} r={(13 * k) / S} fill={WHITE} stroke={OR} strokeWidth={6 / S} />
            <text x={x + lx / S} y={y + ly / S} textAnchor={an as any} fontFamily="Inter" fontWeight={700} fontSize={34 / S} fill={WHITE} opacity={clamp(k)}
              style={{paintOrder: 'stroke', stroke: 'rgba(0,0,0,0.6)', strokeWidth: 6 / S}}>{c}</text>
          </g>;
        })}
      </g>
    </svg>
    <Box y={1400}><Line t0={E.soon} size={38} color="rgba(255,255,255,0.85)" weight={600}>et bientôt Yamoussoukro, Bouaké, Assinie…</Line></Box>
  </AbsoluteFill>;
};

// ================================================================== 5. résidences vérifiées
const FAN = [['vip', 'Korhogo', 'Chambre Salon VIP', '25 000'], ['abidjan', 'Abidjan, Cocody', 'Séjour Abidjan Classique', '40 000'], ['walebo', 'Abidjan, Riviera Palmeraie', 'Les Résidences Le Walebo', '20 000']];
const Verify: React.FC = () => {
  const t = useT(); if (!on(t, 'verify', 0, 0.25)) return null;
  const inK = eOut5(prog(t, SC.verify[0], SC.verify[0] + 0.5));
  const out = eIn(prog(t, E.toAvail, SC.verify[1] + 0.2));
  const sel = E.shots.filter((x: number) => t >= x).length - 1;     // carte mise en avant (flash photo)
  const st = prog(t, E.stamp - 0.1, E.stamp);
  return <AbsoluteFill style={{transform: `scale(${(0.7 + 0.3 * inK) * (1 + out * 2.5)})`, filter: `blur(${out * 20}px)`, opacity: inK * (1 - prog(t, SC.verify[1] + 0.1, SC.verify[1] + 0.25))}}>
    <DarkBG />
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, perspective: 1800}}>
      {FAN.map(([img, loc, name, price], i) => {
        const fan = eOut5(prog(t, E.fan + i * 0.08, E.fan + i * 0.08 + 0.6));
        const isSel = i === sel; const selK = isSel ? eOut5(prog(t, E.shots[i], E.shots[i] + 0.35)) : (sel > i ? 1 : 0) * 0;
        const base = (i - 1);
        const x = CX - 330 + base * 300 * fan * (1 - (isSel ? selK : 0)), ry = -base * 28 * fan * (1 - (isSel ? selK : 0)), z = isSel ? 220 * selK : -80 * Math.abs(base);
        return <div key={img} style={{position: 'absolute', left: x, top: 490, width: 660, height: 850, borderRadius: 44, overflow: 'hidden', background: WHITE,
          transform: `translateZ(${z}px) rotateY(${ry}deg) rotateZ(${base * 4 * fan * (isSel ? 1 - selK : 1)}deg)`, zIndex: isSel ? 10 : 5 - Math.abs(base),
          boxShadow: '0 40px 90px rgba(0,0,0,0.55)'}}>
          <div style={{height: 580, overflow: 'hidden'}}><Img src={staticFile(`img/${img}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1.15 - 0.1 * prog(t, E.fan, SC.verify[1])})`}} /></div>
          <div style={{padding: '24px 34px', fontFamily: BODY}}>
            <div style={{display: 'flex', alignItems: 'center', gap: 8, fontSize: 30, color: '#6b7280'}}><Icon n="pin" s={32} c="#6b7280" />{loc}</div>
            <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 44, color: INK, marginTop: 8}}>{name}</div>
            <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 52, color: OR, marginTop: 8}}>{price} FCFA <span style={{fontSize: 30, color: '#6b7280', fontWeight: 600}}>/nuit</span></div>
          </div>
          {isSel && <AbsoluteFill style={{background: WHITE, opacity: 0.8 * (1 - prog(t, E.shots[i], E.shots[i] + 0.15))}} />}
        </div>;
      })}
    </div>
    {/* tampon géant */}
    {st > 0 && <div style={{position: 'absolute', left: CX - 430, top: 300, width: 860, display: 'flex', justifyContent: 'center',
      transform: `scale(${3.2 - 2.2 * eOut(st)}) rotate(${-8 + 0 * st}deg)`, opacity: clamp(st * 1.5), zIndex: 20}}>
      <div style={{padding: '20px 44px', border: `10px solid ${GREEN}`, borderRadius: 30, background: 'rgba(255,255,255,0.95)', display: 'flex', alignItems: 'center', gap: 18,
        boxShadow: '0 20px 60px rgba(22,163,74,0.45)'}}>
        <Icon n="shield" s={90} c={GREEN} w={2.6} />
        <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 88, color: GREEN, lineHeight: 1}}>100 %<br /><span style={{fontSize: 64}}>VÉRIFIÉES</span></div>
      </div>
    </div>}
    <Box y={1395} style={{zIndex: 30}}><Line t0={E.stampSub} size={40} color={WHITE} weight={700}>Contrôle complet sur place</Line></Box>
    <Particles t0={E.stamp} y={420} n={30} colors={[GREEN, WHITE, GOLD]} dist={600} seed={9} />
  </AbsoluteFill>;
};

// ================================================================== 6. 10 MIN
const Avail: React.FC = () => {
  const t = useT(); if (!on(t, 'avail', 0, 0.25)) return null;
  const out = eIn(prog(t, E.toPay, SC.avail[1] + 0.2));
  const tk = eInOut(prog(t, E.tick[0], E.tick[1]));
  const s10 = sp(t, E.ten, 9, 200), smin = eOut5(prog(t, E.min, E.min + 0.35));
  const nk = eBack(prog(t, E.confirmed, E.confirmed + 0.45), 1.4);
  const R = 360;
  return <AbsoluteFill style={{transform: `translateY(${-out * 1900}px)`, filter: `blur(${out * 20}px)`}}>
    <DarkBG />
    <Box y={240} style={{opacity: 1 - prog(t, E.confirmed - 0.2, E.confirmed)}}><Kinetic text="02 · RÉSERVEZ" t0={SC.avail[0]} size={72} stagger={0.02} /></Box>
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      <g transform={`translate(${CX} 900)`}>
        {Array.from({length: 60}).map((_, i) => {
          const a = (i / 60) * Math.PI * 2 - Math.PI / 2, lit = i / 60 <= tk; const L = i % 5 === 0 ? 34 : 16;
          return <line key={i} x1={Math.cos(a) * (R - L)} y1={Math.sin(a) * (R - L)} x2={Math.cos(a) * R} y2={Math.sin(a) * R} stroke={lit ? OR : 'rgba(255,255,255,0.18)'} strokeWidth={i % 5 === 0 ? 7 : 4} strokeLinecap="round"
            opacity={eOut(prog(t, E.ten + i * 0.004, E.ten + i * 0.004 + 0.2))} />;
        })}
        <circle r={R + 24} fill="none" stroke={OR} strokeWidth={6} strokeDasharray={2 * Math.PI * (R + 24)} strokeDashoffset={2 * Math.PI * (R + 24) * (1 - tk)} transform="rotate(-90)" style={{filter: 'drop-shadow(0 0 14px rgba(245,144,30,0.8))'}} />
      </g>
    </svg>
    <div style={{position: 'absolute', left: CX - 400, top: 640, width: 800, display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 10}}>
      <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 340, color: WHITE, lineHeight: 1, transform: `scale(${0.3 + 0.7 * s10})`}}>10</div>
      <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 120, color: OR, lineHeight: 1, transform: `translateY(${(1 - smin) * 80}px)`, opacity: smin}}>MIN</div>
    </div>
    <Box y={1300}><Line t0={E.min + 0.1} size={46} color={WHITE} weight={700}>pour confirmer la disponibilité</Line></Box>
    {/* notification qui tombe */}
    {t >= E.confirmed && <div style={{position: 'absolute', left: CX - 430, top: 300 + (1 - nk) * -500, width: 860, padding: '26px 30px', borderRadius: 36, background: 'rgba(255,255,255,0.97)',
      boxShadow: '0 30px 70px rgba(0,0,0,0.45)', display: 'flex', alignItems: 'center', gap: 22, fontFamily: BODY, zIndex: 20}}>
      <div style={{width: 84, height: 84, borderRadius: 24, background: GREEN, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon n="check" s={52} c={WHITE} w={3} /></div>
      <div><div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 42, color: INK}}>Disponibilité confirmée</div><div style={{fontSize: 32, color: '#6b7280'}}>par le propriétaire · 10 min max.</div></div>
    </div>}
    <Flare t0={E.ten} y={900} /><Ring t0={E.ten} y={900} r={800} />
  </AbsoluteFill>;
};

// ================================================================== 7. 30 %
const Pay: React.FC = () => {
  const t = useT(); if (!on(t, 'pay', 0.25, 0.25)) return null;
  const inK = eOut5(prog(t, SC.pay[0] - 0.25, SC.pay[0] + 0.2));
  const out = eIn(prog(t, E.toStay, SC.pay[1] + 0.2));
  const fill = eInOut(prog(t, E.fill[0], E.fill[1]));
  const s = sp(t, E.thirty, 9, 210);
  return <AbsoluteFill style={{transform: `translateY(${(1 - inK) * 1900}px) translateX(${out * 1300}px)`, filter: `blur(${out * 22}px)`}}>
    <AbsoluteFill style={{background: `linear-gradient(160deg, ${OR} 0%, ${OR2} 100%)`}} />
    <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 35%, rgba(255,255,255,0.25), transparent 55%)'}} />
    <div style={{position: 'absolute', left: CX - 470, top: 380, width: 940, height: 420, transform: `scale(${0.3 + 0.7 * s})`}}>
      {/* contour + remplissage qui monte */}
      <div style={{position: 'absolute', inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', fontFamily: HEAD, fontWeight: 900, fontSize: 340, lineHeight: 1, color: 'transparent', WebkitTextStroke: '6px #fff', letterSpacing: -10}}>30 %</div>
      <div style={{position: 'absolute', inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', fontFamily: HEAD, fontWeight: 900, fontSize: 340, lineHeight: 1, color: '#fff', letterSpacing: -10,
        clipPath: `inset(${(1 - fill) * 100}% 0 0 0)`}}>30 %</div>
    </div>
    <Box y={860}><Kinetic text="d’acompte sécurisé" t0={E.deposit} size={76} stagger={0.018} /></Box>
    {[['mobile', 'Mobile Money'], ['wallet', 'Portefeuille ResyFlex']].map(([ic, lab], i) => {
      const k = eBack(prog(t, E.chips[i], E.chips[i] + 0.35), 2.2); if (t < E.chips[i]) return null;
      return <div key={lab} style={{position: 'absolute', left: CX - 360, top: 1030 + i * 140, width: 720, height: 116, borderRadius: 60, background: INK, display: 'flex', alignItems: 'center', gap: 22, padding: '0 34px',
        transform: `scale(${k})`, opacity: clamp(k * 2), boxShadow: '0 20px 50px rgba(0,0,0,0.3)'}}>
        <div style={{width: 70, height: 70, borderRadius: 35, background: OR, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon n={ic} s={40} c={WHITE} w={2.4} /></div>
        <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 42, color: WHITE}}>{lab}</span>
      </div>;
    })}
    <Box y={1340}><Line t0={E.coins} size={50} color={INK} weight={800} font={HEAD}>Le reste se règle à l’arrivée</Line></Box>
    <Particles t0={E.coins} y={1200} n={34} colors={[GOLD, '#fff3c4', '#e0a020']} dist={560} seed={21} />
  </AbsoluteFill>;
};

// ================================================================== 8. séjournez : QR Code
const QR: React.FC<{t: number}> = ({t}) => {
  const N = 21; const r = rng(17); const cells: React.ReactNode[] = [];
  const finder = (y: number, x: number) => { for (const [fy, fx] of [[0, 0], [0, N - 7], [N - 7, 0]]) { const a = y - fy, b = x - fx; if (a >= 0 && a < 7 && b >= 0 && b < 7) return (a === 0 || a === 6 || b === 0 || b === 6 || (a >= 2 && a <= 4 && b >= 2 && b <= 4)) ? 1 : 0; } return -1; };
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const f = finder(y, x); const v = f === -1 ? r() > 0.5 : f === 1; const ap = E.qrBuild[0] + r() * (E.qrBuild[1] - E.qrBuild[0]); if (!v) continue;
    const k = eBack(prog(t, ap, ap + 0.15)); cells.push(<rect key={y * N + x} x={x * 14 + 7 * (1 - k)} y={y * 14 + 7 * (1 - k)} width={14 * k} height={14 * k} rx={2} fill={INK} />);
  }
  return <svg width={294} height={294} viewBox="0 0 294 294">{cells}</svg>;
};
const Stay: React.FC = () => {
  const t = useT(); if (!on(t, 'stay', 0, 0.25)) return null;
  const inK = eOut5(prog(t, SC.stay[0], SC.stay[0] + 0.6)); const out = eIn(prog(t, E.toTrust, SC.stay[1] + 0.2));
  const ok = t >= E.scanOk; const sk = prog(t, E.scan[0], E.scan[1]);
  const rays = eOut(prog(t, E.welcome, E.welcome + 0.8));
  return <AbsoluteFill style={{transform: `scale(${1 + out * 3})`, filter: `blur(${out * 20}px)`, opacity: 1 - prog(t, SC.stay[1] + 0.05, SC.stay[1] + 0.25)}}>
    <DarkBG hue={ok ? GREEN : OR} />
    {/* rayons de lumière à l'accueil */}
    {rays > 0 && <AbsoluteFill style={{background: `conic-gradient(from ${t * 20}deg at ${CX}px 1000px, ${[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => `rgba(255,200,110,${i % 2 ? 0 : 0.22 * rays}) ${i * 30}deg ${(i + 1) * 30}deg`).join(',')})`, mixBlendMode: 'screen'}} />}
    <Box y={240}><Kinetic text="03 · SÉJOURNEZ" t0={SC.stay[0] + 0.1} size={72} stagger={0.02} /></Box>
    <Phone3D x={CX} y={1010 + (1 - inK) * 700} w={430} ry={(1 - inK) * 40 + 6 * Math.sin((t - 28) * 1.1)} rx={(1 - inK) * 10}>
      <AbsoluteFill style={{background: ok ? '#ecfdf3' : WHITE, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 150, fontFamily: BODY}}>
        <Img src={staticFile('img/logo-full.png')} style={{width: 230}} />
        <div style={{marginTop: 50, position: 'relative', padding: 18, borderRadius: 24, border: `6px solid ${ok ? GREEN : '#e5e7eb'}`, background: WHITE}}>
          <QR t={t} />
          {sk > 0 && sk < 1 && <div style={{position: 'absolute', left: -10, right: -10, top: 18 + 294 * sk - 3, height: 6, background: OR, boxShadow: '0 0 26px 8px rgba(245,144,30,0.7)', borderRadius: 3}} />}
        </div>
        <div style={{marginTop: 40, fontFamily: HEAD, fontWeight: 800, fontSize: 34, color: ok ? GREEN : INK}}>{ok ? 'Réservation validée ✓' : 'Votre QR Code'}</div>
      </AbsoluteFill>
    </Phone3D>
    <Box y={1500} style={{zIndex: 10}}><Line t0={E.scanOk} size={46} weight={800} font={HEAD}>Arrivée validée par QR Code</Line></Box>
    {t >= E.welcome && <Box y={380} style={{zIndex: 10}}><Kinetic text="Bienvenue chez vous" t0={E.welcome} size={70} color={GOLD} stagger={0.018} /></Box>}
    <Ring t0={E.scanOk} y={1000} r={700} c={GREEN} />
    <Particles t0={E.scanOk} y={1000} n={36} colors={[GREEN, GOLD, WHITE]} dist={560} seed={33} />
  </AbsoluteFill>;
};

// ================================================================== 9. engagements en rafale
const TRUST: [string, string, string, string][] = [['shield', 'Vérifiées', 'sur place', OR], ['lock', 'Acompte', 'protégé', INK], ['refresh', 'Remboursé', 'jusqu’à 48 h avant', CREAM], ['star', 'Avis', 'authentiques', OR]];
const Trust: React.FC = () => {
  const t = useT(); if (!on(t, 'trust')) return null;
  const i = Math.min(3, E.trust.filter((x: number) => t >= x).length - 1); const [ic, a, b, bg] = TRUST[i]; const t0 = E.trust[i];
  const fg = bg === CREAM ? INK : WHITE; const ac = bg === OR ? INK : OR;
  const k = sp(t, t0, 10, 260);
  return <AbsoluteFill style={{background: bg}}>
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, rgba(255,255,255,${bg === INK ? 0.06 : 0.22}), transparent 60%)`}} />
    <Box y={560}>
      <div style={{width: 230, height: 230, borderRadius: 70, background: bg === OR ? INK : OR, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k}) rotate(${(1 - k) * -25}deg)`}}>
        <Icon n={ic} s={140} c={WHITE} w={2.2} /></div>
      <div style={{marginTop: 50, fontFamily: HEAD, fontWeight: 900, fontSize: 150, color: fg, lineHeight: 1, transform: `scale(${0.6 + 0.4 * k})`}}>{a}</div>
      <div style={{marginTop: 10, fontFamily: HEAD, fontWeight: 900, fontSize: b.length > 12 ? 68 : 104, color: ac, lineHeight: 1, transform: `translateY(${(1 - k) * 60}px)`}}>{b}</div>
    </Box>
  </AbsoluteFill>;
};

// ================================================================== 10. propriétaires
const Owner: React.FC = () => {
  const t = useT(); if (!on(t, 'owner')) return null;
  const k = eOut5(prog(t, SC.owner[0], SC.owner[0] + 0.35)); const g = eBack(prog(t, E.owner[2], E.owner[2] + 0.35), 2);
  const suck = eIn(prog(t, TL.music.cut[0], SC.owner[1]));
  return <AbsoluteFill style={{clipPath: `circle(${k * 150}% at ${CX}px 960px)`, transform: `scale(${1 - suck * 0.6})`, opacity: 1 - suck}}>
    <KenBurns src="angre" t0={SC.owner[0]} dur={2} from={1.3} to={1.1} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(17,20,27,0.75), rgba(17,20,27,0.55) 50%, rgba(17,20,27,0.85))'}} />
    <Box y={560}><Kinetic text="Propriétaire ?" t0={E.owner[0] + 0.05} size={118} stagger={0.02} /></Box>
    <Box y={720}><Kinetic text="Publiez votre résidence" t0={E.owner[1]} size={64} color={GOLD} weight={800} stagger={0.015} /></Box>
    {t >= E.owner[2] && <Box y={900}><div style={{padding: '26px 56px', borderRadius: 70, background: OR, transform: `scale(${g})`, boxShadow: '0 20px 60px rgba(245,144,30,0.55)'}}>
      <span style={{fontFamily: HEAD, fontWeight: 900, fontSize: 64, color: WHITE}}>Inscription gratuite</span></div></Box>}
  </AbsoluteFill>;
};

// ================================================================== 11. appel à l'action
const CTA: React.FC = () => {
  const t = useT(); if (!on(t, 'cta')) return null;
  const s = sp(t, E.ctaHit, 9, 170); const u = eBack(prog(t, E.ctaUrl, E.ctaUrl + 0.4), 2); const ph = eOut5(prog(t, E.ctaPhone, E.ctaPhone + 0.4));
  return <AbsoluteFill>
    <CreamBG />
    <Ring t0={E.ctaHit} y={760} r={1100} /><Ring t0={E.ctaHit + 0.08} y={760} r={800} c={GOLD} w={12} /><Ring t0={E.ctaHit + 0.16} y={760} r={550} c={OR2} w={8} />
    <div style={{position: 'absolute', left: CX - 450, top: 620, width: 900, transform: `scale(${0.3 + 0.7 * s})`}}><Img src={staticFile('img/logo-full.png')} style={{width: 900}} /></div>
    <Box y={910}><Kinetic text="Trouvez · Réservez · Séjournez" t0={E.ctaTag} size={54} color={INK} weight={800} stagger={0.012} spacing={0} /></Box>
    {t >= E.ctaUrl && <Box y={1060}><div style={{padding: '28px 64px', borderRadius: 80, background: `linear-gradient(90deg, ${OR}, ${OR2})`, transform: `scale(${u})`, boxShadow: '0 24px 60px rgba(245,144,30,0.5)'}}>
      <span style={{fontFamily: HEAD, fontWeight: 900, fontSize: 76, color: WHITE}}>resy-flex.com</span></div></Box>}
    <Box y={1260}><div style={{display: 'flex', alignItems: 'center', gap: 16, opacity: ph, transform: `translateY(${(1 - ph) * 30}px)`}}><Icon n="phone" s={52} c={OR} w={2.4} />
      <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 50, color: INK}}>+225 01 01 01 46 04</span></div></Box>
    <Particles t0={E.ctaHit + 0.1} y={760} n={60} dist={800} seed={51} />
    <Flash t0={E.ctaHit} d={0.3} a={0.9} />
    <Flare t0={E.ctaHit + 0.05} y={760} />
  </AbsoluteFill>;
};

// ================================================================== composition
export const ResyFlex: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <Audio src={staticFile('audio/mix.wav')} />
    <Camera>
      <Hook /><Logo /><Find /><MapScene /><Verify /><Avail /><Pay /><Stay /><Trust /><Owner /><CTA />
    </Camera>
    <LightLeaks />
    <Grain />
    <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
    <AbsoluteFill style={{background: '#000', opacity: prog(t, E.fade, TL.duration)}} />
  </AbsoluteFill>;
};
