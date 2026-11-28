import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing, spring, delayRender, continueRender} from 'remotion';
import TL from './timeline.json';

// ------------------------------------------------------------------ charte ResyFlex (relevée sur resy-flex.com)
const OR = '#f5901e', OR2 = '#ff7a1a', INK = '#1f2430', MUT = '#6b7280', CREAM = '#fff7ee', GREEN = '#16a34a', BLUE = '#2563eb';
const HEAD = 'Poppins, sans-serif', BODY = 'Inter, sans-serif';
const CX = 510;                 // centre de la zone de sécurité (bande droite de 120 px réservée aux boutons)
const E: any = TL.ev, SC: any = TL.scenes;

// ------------------------------------------------------------------ polices locales
const fontHandle = delayRender('fonts');
const faces: [string, string, string][] = [
  ['Poppins', '600', 'poppins-latin-600-normal.woff2'], ['Poppins', '700', 'poppins-latin-700-normal.woff2'],
  ['Poppins', '800', 'poppins-latin-800-normal.woff2'], ['Poppins', '900', 'poppins-latin-900-normal.woff2'],
  ['Inter', '400', 'inter-latin-400-normal.woff2'], ['Inter', '500', 'inter-latin-500-normal.woff2'],
  ['Inter', '600', 'inter-latin-600-normal.woff2'], ['Inter', '700', 'inter-latin-700-normal.woff2'],
];
Promise.all(faces.map(([fam, w, file]) => new FontFace(fam, `url(${staticFile('fonts/' + file)})`, {weight: w}).load().then((ff) => (document as any).fonts.add(ff))))
  .then(() => continueRender(fontHandle)).catch(() => continueRender(fontHandle));

// ------------------------------------------------------------------ outils d'animation
const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
const eOut = (k: number) => Easing.out(Easing.cubic)(clamp(k));
const eIn = (k: number) => Easing.in(Easing.cubic)(clamp(k));
const eBack = (k: number) => Easing.out(Easing.back(1.8))(clamp(k));
const useT = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
// ressort calculé à partir du temps (fonction pure, pas un hook : utilisable après un return conditionnel)
const springAt = (t: number, t0: number, cfg = {damping: 11, stiffness: 170, mass: 0.8}) =>
  spring({frame: Math.round((t - t0) * TL.fps), fps: TL.fps, config: cfg});
const inScene = (t: number, k: string, pre = 0, post = 0) => t >= SC[k][0] - pre && t < SC[k][1] + post;
// sortie de scène : léger recul + fondu sur les 0,25 dernières secondes
const outK = (t: number, k: string, d = 0.25) => eIn(prog(t, SC[k][1] - d, SC[k][1]));

// ------------------------------------------------------------------ icônes (traits simples)
const Icon: React.FC<{name: string; size?: number; color?: string; stroke?: number}> = ({name, size = 48, color = INK, stroke = 2.2}) => {
  const p: any = {fill: 'none', stroke: color, strokeWidth: stroke, strokeLinecap: 'round', strokeLinejoin: 'round'};
  const shapes: Record<string, React.ReactNode> = {
    pin: <><path {...p} d="M12 21s-7-6.5-7-11a7 7 0 0 1 14 0c0 4.5-7 11-7 11z" /><circle {...p} cx="12" cy="10" r="2.5" /></>,
    search: <><circle {...p} cx="11" cy="11" r="7" /><path {...p} d="M16.5 16.5L21 21" /></>,
    calendar: <><rect {...p} x="3" y="5" width="18" height="16" rx="2.5" /><path {...p} d="M3 10h18M8 3v4M16 3v4" /></>,
    lock: <><rect {...p} x="5" y="11" width="14" height="10" rx="2" /><path {...p} d="M8 11V8a4 4 0 0 1 8 0v3" /></>,
    shield: <><path {...p} d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" /><path {...p} d="M8.5 12l2.5 2.5 4.5-5" /></>,
    refresh: <><path {...p} d="M20 12a8 8 0 1 1-2.4-5.7" /><path {...p} d="M20 4v5h-5" /></>,
    star: <polygon {...p} points="12,3 14.8,9 21,9.6 16.2,13.8 17.6,20 12,16.8 6.4,20 7.8,13.8 3,9.6 9.2,9" />,
    home: <><path {...p} d="M3 11l9-8 9 8" /><path {...p} d="M5 10v10h14V10" /><path {...p} d="M10 20v-6h4v6" /></>,
    phone: <path {...p} d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" />,
    check: <path {...p} d="M5 12.5l4.5 4.5L19 7.5" />,
    wallet: <><rect {...p} x="3" y="6" width="18" height="13" rx="2.5" /><path {...p} d="M3 10h18M16 14.5h2" /></>,
    mobile: <><rect {...p} x="7" y="2.5" width="10" height="19" rx="2.2" /><path {...p} d="M11 18.5h2" /></>,
    nav: <polygon {...p} points="3,11 21,3 13,21 11,13" />,
    bed: <><path {...p} d="M3 18V7M3 13h18v5M21 18v-3a3 3 0 0 0-3-3h-8v1" /><circle {...p} cx="7" cy="10.5" r="1.6" /></>,
    clock: <><circle {...p} cx="12" cy="12" r="8.5" /><path {...p} d="M12 7.5V12l3 2" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24">{shapes[name]}</svg>;
};

// ------------------------------------------------------------------ éléments récurrents
const Txt: React.FC<{children: React.ReactNode; size: number; weight?: number; color?: string; font?: string; style?: React.CSSProperties}> =
  ({children, size, weight = 800, color = INK, font = HEAD, style}) =>
    <div style={{fontFamily: font, fontWeight: weight, fontSize: size, color, lineHeight: 1.1, letterSpacing: font === HEAD ? -0.5 : 0, ...style}}>{children}</div>;

const Center: React.FC<{y: number; children: React.ReactNode; style?: React.CSSProperties; w?: number}> = ({y, children, style, w = 880}) =>
  <div style={{position: 'absolute', left: CX - w / 2, top: y, width: w, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', ...style}}>{children}</div>;

const CreamBG: React.FC = () => {
  const t = useT();
  const b = (x: number, y: number, r: number, c: string, ph: number) =>
    <div style={{position: 'absolute', left: x + 60 * Math.sin(t * 0.6 + ph) - r, top: y + 50 * Math.cos(t * 0.5 + ph) - r, width: 2 * r, height: 2 * r,
      borderRadius: '50%', background: `radial-gradient(circle, ${c} 0%, rgba(255,255,255,0) 70%)`}} />;
  return <AbsoluteFill style={{background: CREAM, overflow: 'hidden'}}>
    {b(120, 260, 520, 'rgba(245,144,30,0.22)', 0)}{b(980, 1500, 640, 'rgba(245,144,30,0.18)', 2)}{b(900, 300, 380, 'rgba(255,200,140,0.35)', 4)}
  </AbsoluteFill>;
};

const Heading: React.FC<{t0: number; title: string; sub?: string; y?: number; color?: string}> = ({t0, title, sub, y = 250, color = INK}) => {
  const t = useT(); const k = eOut(prog(t, t0, t0 + 0.35)); const ks = eOut(prog(t, t0 + 0.15, t0 + 0.5));
  return <Center y={y}>
    <Txt size={72} color={color} style={{opacity: k, transform: `translateY(${(1 - k) * 40}px)`}}>{title}</Txt>
    {sub && <Txt size={42} weight={600} font={BODY} color={OR} style={{marginTop: 14, opacity: ks, transform: `translateY(${(1 - ks) * 30}px)`}}>{sub}</Txt>}
  </Center>;
};

const Phone: React.FC<{x: number; y: number; w: number; h: number; children: React.ReactNode; style?: React.CSSProperties}> = ({x, y, w, h, children, style}) =>
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 64, background: '#11141b', padding: 16,
    boxShadow: '0 40px 90px rgba(31,36,48,0.35)', ...style}}>
    <div style={{width: '100%', height: '100%', borderRadius: 50, background: '#f7f8fa', overflow: 'hidden', position: 'relative'}}>
      <div style={{position: 'absolute', top: 14, left: '50%', transform: 'translateX(-50%)', width: 150, height: 34, borderRadius: 20, background: '#11141b', zIndex: 5}} />
      {children}
    </div>
  </div>;

// rideau orange de chapitre : 01 TROUVEZ / 02 RÉSERVEZ / 03 SÉJOURNEZ
const Chapter: React.FC<{t0: number; num: string; word: string}> = ({t0, num, word}) => {
  const t = useT(); if (t < t0 - 0.05 || t > t0 + 0.9) return null;
  const inK = eOut(prog(t, t0 - 0.05, t0 + 0.2)), outK2 = eIn(prog(t, t0 + 0.6, t0 + 0.85));
  const wk = eBack(prog(t, t0 + 0.05, t0 + 0.35));
  return <AbsoluteFill style={{clipPath: `polygon(0 ${100 - inK * 130}%, 100% ${100 - inK * 130 + 30}%, 100% ${100 - outK2 * 130}%, 0 ${100 - outK2 * 130 + 30}%)`.replace(/(\d+(\.\d+)?)%/g, (m) => m)}}>
    <AbsoluteFill style={{background: `linear-gradient(160deg, ${OR} 0%, ${OR2} 100%)`}} />
    <Center y={700}>
      <Txt size={220} weight={900} color="rgba(255,255,255,0.25)" style={{transform: `translateY(${(1 - wk) * 80}px)`}}>{num}</Txt>
      <Txt size={128} weight={900} color="#fff" style={{marginTop: -60, letterSpacing: 2, transform: `scale(${0.6 + 0.4 * wk})`}}>{word}</Txt>
    </Center>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 1. accroche
const Hook: React.FC = () => {
  const t = useT(); if (!inScene(t, 'hook')) return null;
  const up = eOut(prog(t, 1.9, 2.3));
  const words: [string, number, string?][] = [['Tu cherches', E.hookWords[0]], ['une résidence meublée', E.hookWords[1]], ['en Côte d’Ivoire', E.hookWords[2], OR]];
  const q = eBack(prog(t, E.hookWords[3], E.hookWords[3] + 0.3));
  const photos = ['hook1', 'hook2', 'hook3'];
  const zoom = eIn(prog(t, 3.55, 4.0));
  return <AbsoluteFill style={{background: '#12151c', overflow: 'hidden'}}>
    <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 40%, rgba(245,144,30,0.25), rgba(0,0,0,0) 60%)'}} />
    {photos.map((p, i) => {
      const t0 = E.hookPhotos[i]; const k = eOut(prog(t, t0 - 0.12, t0)); if (t < t0 - 0.12) return null;
      const rot = [-7, 5, -2][i]; const sc = (1.5 - 0.5 * k) * (i === 2 ? 1 + zoom * 1.6 : 1);
      return <div key={p} style={{position: 'absolute', left: CX - 330, top: 760 + i * 20, width: 660, height: 860, borderRadius: 44, overflow: 'hidden',
        transform: `rotate(${rot * (1 - (i === 2 ? zoom : 0))}deg) scale(${sc})`, opacity: k, boxShadow: '0 30px 80px rgba(0,0,0,0.5)', border: '10px solid #fff'}}>
        <Img src={staticFile(`img/${p}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </div>;
    })}
    <div style={{position: 'absolute', left: 0, top: 0, width: '100%', transform: `translateY(${interpolate(up, [0, 1], [0, -380])}px) scale(${1 - 0.18 * up})`, transformOrigin: `${CX}px 300px`}}>
      <Center y={720}>
        {words.map(([w, t0, c], i) => {
          const k = eBack(prog(t, t0, t0 + 0.28));
          return <div key={i} style={{position: 'relative', opacity: clamp(k * 1.5), transform: `translateY(${(1 - k) * 60}px)`, marginTop: 8}}>
            {c && <div style={{position: 'absolute', left: -16, right: -16, top: 18, bottom: 6, background: 'rgba(245,144,30,0.22)', borderRadius: 14,
              transform: `scaleX(${eOut(prog(t, t0 + 0.1, t0 + 0.45))})`, transformOrigin: 'left'}} />}
            <Txt size={92} color={c || '#fff'} style={{position: 'relative'}}>{w}{i === 2 && <span style={{display: 'inline-block', color: OR, transform: `scale(${q}) rotate(${(1 - q) * 30}deg)`, marginLeft: 8}}>?</span>}</Txt>
          </div>;
        })}
      </Center>
    </div>
    <AbsoluteFill style={{background: '#fff', opacity: prog(t, 3.8, 4.0)}} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 2. logo
const Logo: React.FC = () => {
  const t = useT(); if (!inScene(t, 'logo')) return null;
  const s = springAt(t, E.logoHit); const rev = eOut(prog(t, E.logoHit + 0.1, E.logoHit + 0.6)); const o = outK(t, 'logo');
  const flash = 1 - prog(t, E.logoHit, E.logoHit + 0.35);
  const rings = [0, 0.08].map((d, i) => {
    const k = prog(t, E.logoHit + d, E.logoHit + d + 0.7); if (k <= 0 || k >= 1) return null;
    return <div key={i} style={{position: 'absolute', left: CX - 600 * eOut(k), top: 720 - 600 * eOut(k), width: 1200 * eOut(k), height: 1200 * eOut(k),
      borderRadius: '50%', border: `${14 * (1 - k)}px solid ${OR}`, opacity: 1 - k}} />;
  });
  const promise = ['Trouvez', 'Réservez', 'Séjournez'];
  return <AbsoluteFill style={{transform: `scale(${1 - 0.08 * o})`, opacity: 1 - o}}>
    <CreamBG />{rings}
    <div style={{position: 'absolute', left: CX - 440, top: 620, width: 880, transform: `scale(${0.55 + 0.45 * s})`}}>
      <div style={{clipPath: `inset(0 ${(1 - rev) * 62}% 0 0)`}}>
        <Img src={staticFile('img/logo-full.png')} style={{width: 880}} />
      </div>
    </div>
    <Center y={900}>
      <Txt size={48} weight={600} font={BODY} color={INK} style={{opacity: eOut(prog(t, E.slogan, E.slogan + 0.4)), transform: `translateY(${(1 - eOut(prog(t, E.slogan, E.slogan + 0.4))) * 30}px)`}}>
        Résidences meublées<br />en Côte d’Ivoire</Txt>
    </Center>
    {promise.map((w, i) => {
      const k = eBack(prog(t, E.promise[i], E.promise[i] + 0.3));
      return <div key={w} style={{position: 'absolute', left: CX - 230, top: 1080 + i * 125, width: 460, height: 100, borderRadius: 60,
        background: i === 2 ? OR : '#fff', border: `4px solid ${OR}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
        transform: `scale(${k})`, opacity: clamp(k * 2), boxShadow: '0 12px 30px rgba(245,144,30,0.25)'}}>
        <Txt size={52} weight={800} color={i === 2 ? '#fff' : OR}>{w}</Txt>
      </div>;
    })}
    <AbsoluteFill style={{background: '#fff', opacity: flash * 0.9}} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 3. trouvez : recherche
const CITIES = ['Abidjan', 'San-Pedro', 'Korhogo', 'Grand-Bassam', 'Bingerville', 'Boundiali', 'Grand-Lahou'];
const Find: React.FC = () => {
  const t = useT(); if (!inScene(t, 'find')) return null;
  const ph = springAt(t, E.phoneIn - 0.25, {damping: 16, stiffness: 120, mass: 1}); const o = outK(t, 'find');
  const typed = 'Abidjan'.slice(0, Math.max(0, Math.floor((t - E.typeStart) / 0.1)));
  const near = t >= E.nearMe; const nk = eBack(prog(t, E.nearMe, E.nearMe + 0.3));
  const res = eOut(prog(t, E.results, E.results + 0.5));
  return <AbsoluteFill style={{transform: `translateX(${-o * 200}px)`, opacity: 1 - o}}>
    <CreamBG />
    <Heading t0={SC.find[0] + 0.55} title="Partout en" sub="Côte d’Ivoire" y={240} />
    <Phone x={CX - 310} y={interpolate(ph, [0, 1], [1950, 520])} w={620} h={1180}>
      <div style={{padding: '70px 30px 0', fontFamily: BODY}}>
        <Img src={staticFile('img/logo-full.png')} style={{width: 250}} />
        <div style={{marginTop: 26, height: 92, borderRadius: 46, background: '#fff', boxShadow: '0 8px 24px rgba(0,0,0,0.08)', display: 'flex', alignItems: 'center', padding: '0 26px', gap: 16}}>
          <Icon name="pin" size={40} color={OR} />
          <span style={{fontSize: 34, fontWeight: 600, color: typed ? INK : MUT}}>{typed || 'Où allez-vous ?'}{t > E.typeStart && t < E.chips[0] && Math.floor(t * 6) % 2 === 0 ? '|' : ''}</span>
          <div style={{marginLeft: 'auto', width: 64, height: 64, borderRadius: 32, background: OR, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon name="search" size={34} color="#fff" /></div>
        </div>
        <div style={{display: 'flex', flexWrap: 'wrap', gap: 14, marginTop: 30}}>
          {CITIES.map((c, i) => {
            const k = eBack(prog(t, E.chips[i], E.chips[i] + 0.28));
            return <div key={c} style={{padding: '14px 24px', borderRadius: 40, background: i === 0 ? OR : '#fff', color: i === 0 ? '#fff' : INK,
              border: `3px solid ${i === 0 ? OR : '#e5e7eb'}`, fontSize: 32, fontWeight: 600, transform: `scale(${k})`, opacity: clamp(k * 2)}}>{c}</div>;
          })}
        </div>
        <div style={{marginTop: 26, display: 'inline-flex', alignItems: 'center', gap: 12, padding: '14px 24px', borderRadius: 40,
          background: near ? '#e8efff' : '#fff', border: `3px solid ${near ? BLUE : '#e5e7eb'}`, transform: `scale(${t < E.nearMe ? 0.001 + eBack(prog(t, E.chips[6] + 0.1, E.chips[6] + 0.4)) : 1 + 0.12 * (1 - nk) * (nk > 0 ? 1 : 0)})`}}>
          <Icon name="nav" size={32} color={near ? BLUE : MUT} />
          <span style={{fontSize: 32, fontWeight: 600, color: near ? BLUE : MUT}}>Autour de moi · 10 km</span>
        </div>
        <div style={{marginTop: 30, display: 'flex', gap: 18, transform: `translateY(${(1 - res) * 300}px)`, opacity: res}}>
          {['classique', 'walebo'].map((p) => <div key={p} style={{flex: 1, height: 300, borderRadius: 28, overflow: 'hidden', boxShadow: '0 10px 24px rgba(0,0,0,0.12)'}}>
            <Img src={staticFile(`img/${p}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>)}
        </div>
      </div>
    </Phone>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 4. résidences vérifiées
const CARDS = [
  {img: 'classique', loc: 'Abidjan, Cocody', name: 'Séjour Abidjan Classique', rooms: '3 pièces · 2 ch. · 2 sdb.', price: '40 000'},
  {img: 'vip', loc: 'Korhogo', name: 'Chambre Salon VIP', rooms: '2 pièces · 1 ch. · 1 sdb.', price: '25 000'},
  {img: 'walebo', loc: 'Abidjan, Riviera Palmeraie', name: 'Les Résidences Le Walebo', rooms: '1 pièce · 1 ch. · 1 sdb.', price: '20 000'},
];
const Verify: React.FC = () => {
  const t = useT(); if (!inScene(t, 'verify')) return null;
  const o = outK(t, 'verify');
  const st = prog(t, E.stamp - 0.12, E.stamp); const shake = t > E.stamp ? 14 * Math.exp(-(t - E.stamp) * 9) * Math.sin((t - E.stamp) * 70) : 0;
  return <AbsoluteFill style={{opacity: 1 - o, transform: `scale(${1 - 0.06 * o})`}}>
    <CreamBG />
    <Heading t0={SC.verify[0] + 0.05} title="Des résidences" sub="vérifiées sur place" y={240} />
    {CARDS.map((c, i) => {
      const tin = E.cards[i], tout = E.cards[i + 1] ?? 99;
      const kin = eOut(prog(t, tin - 0.18, tin + 0.12)), kout = eIn(prog(t, tout - 0.18, tout + 0.05));
      if (t < tin - 0.2 || kout >= 1) return null;
      const x = (1 - kin) * 900 - kout * 1000, rot = (1 - kin) * 10 - kout * 10;
      return <div key={c.img} style={{position: 'absolute', left: CX - 390 + x, top: 460, width: 780, height: 960, borderRadius: 44, background: '#fff', overflow: 'hidden',
        transform: `rotate(${rot}deg) translateX(${i === 2 ? shake : 0}px)`, boxShadow: '0 30px 70px rgba(31,36,48,0.22)'}}>
        <div style={{height: 580, overflow: 'hidden', position: 'relative'}}>
          <Img src={staticFile(`img/${c.img}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1.08 - 0.08 * prog(t, tin, tin + 1.5)})`}} />
          {i === 2 && st > 0 && <div style={{position: 'absolute', left: 40, top: 40, padding: '18px 34px', borderRadius: 50, background: GREEN, display: 'flex', alignItems: 'center', gap: 12,
            transform: `scale(${3 - 2 * eOut(st)}) rotate(${-12 + 6 * eOut(st)}deg)`, opacity: st, boxShadow: '0 10px 30px rgba(22,163,74,0.5)'}}>
            <Icon name="shield" size={46} color="#fff" stroke={2.6} /><Txt size={46} weight={800} color="#fff">Vérifiée</Txt></div>}
        </div>
        <div style={{padding: '30px 40px', fontFamily: BODY}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 10, color: MUT, fontSize: 32}}><Icon name="pin" size={34} color={MUT} />{c.loc}</div>
          <Txt size={50} weight={800} style={{marginTop: 12}}>{c.name}</Txt>
          <div style={{display: 'flex', alignItems: 'center', gap: 10, color: MUT, fontSize: 32, marginTop: 12}}><Icon name="bed" size={36} color={MUT} />{c.rooms}</div>
          <div style={{marginTop: 18, fontFamily: HEAD, fontWeight: 800, fontSize: 56, color: OR}}>{c.price} FCFA <span style={{fontSize: 32, color: MUT, fontWeight: 600}}>/nuit</span></div>
        </div>
      </div>;
    })}
    <Center y={1446} style={{opacity: eOut(prog(t, E.stampText, E.stampText + 0.3))}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14}}><Icon name="check" size={46} color={GREEN} stroke={3} /><Txt size={40} weight={600} font={BODY}>Contrôle complet en présentiel</Txt></div>
    </Center>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 5. disponibilité
const Avail: React.FC = () => {
  const t = useT(); if (!inScene(t, 'avail')) return null;
  const o = outK(t, 'avail');
  const a = 12, b = 15; const firstDow = 1; // décembre 2026 commence un mardi (L=0)
  const fill = eOut(prog(t, E.dayOut, E.dayOut + 0.3));
  const sentK = eBack(prog(t, E.sent, E.sent + 0.3));
  const tk = prog(t, E.timer[0], E.timer[1]); const ok = t >= E.confirmed; const okK = eBack(prog(t, E.confirmed, E.confirmed + 0.35));
  const cal = eOut(prog(t, SC.avail[0] + 0.5, SC.avail[0] + 0.85));
  return <AbsoluteFill style={{opacity: 1 - o, transform: `translateX(${-o * 200}px)`}}>
    <CreamBG />
    <Heading t0={SC.avail[0] + 0.6} title="Disponibilité" sub="confirmée en 10 min max." y={240} />
    <div style={{position: 'absolute', left: CX - 420, top: 510, width: 840, padding: 36, borderRadius: 44, background: '#fff', boxShadow: '0 24px 60px rgba(31,36,48,0.15)',
      fontFamily: BODY, transform: `translateY(${(1 - cal) * 120}px)`, opacity: cal}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14}}><Icon name="calendar" size={44} color={OR} /><Txt size={44} weight={700}>Décembre 2026</Txt></div>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', marginTop: 22, rowGap: 8, textAlign: 'center'}}>
        {['L', 'M', 'M', 'J', 'V', 'S', 'D'].map((d, i) => <div key={i} style={{fontSize: 28, color: MUT, fontWeight: 600}}>{d}</div>)}
        {Array.from({length: firstDow}).map((_, i) => <div key={'e' + i} />)}
        {Array.from({length: 31}, (_, i) => i + 1).map((d) => {
          const isA = d === a && t >= E.dayIn, isB = d === b && t >= E.dayOut, mid = d > a && d < b && fill > (d - a) / (b - a) - 0.2;
          const pk = d === a ? eBack(prog(t, E.dayIn, E.dayIn + 0.25)) : d === b ? eBack(prog(t, E.dayOut, E.dayOut + 0.25)) : 1;
          return <div key={d} style={{height: 76, display: 'flex', alignItems: 'center', justifyContent: 'center', background: mid ? 'rgba(245,144,30,0.18)' : 'transparent'}}>
            <div style={{width: 70, height: 70, borderRadius: 35, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32, fontWeight: 700,
              background: isA || isB ? OR : 'transparent', color: isA || isB ? '#fff' : INK, transform: `scale(${isA || isB ? pk : 1})`}}>{d}</div></div>;
        })}
      </div>
      <div style={{marginTop: 20, height: 92, borderRadius: 46, background: t >= E.sent ? GREEN : OR, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14,
        transform: `scale(${t >= E.sent ? 0.9 + 0.1 * sentK : 1})`}}>
        {t >= E.sent && <Icon name="check" size={40} color="#fff" stroke={3} />}
        <Txt size={40} weight={700} color="#fff" font={BODY}>{t >= E.sent ? 'Demande envoyée' : 'Demander la disponibilité'}</Txt>
      </div>
    </div>
    {t >= E.timer[0] - 0.1 && <div style={{position: 'absolute', left: CX - 420, top: 1290, width: 840, height: 190, borderRadius: 40, background: ok ? '#ecfdf3' : '#fff',
      boxShadow: '0 18px 40px rgba(31,36,48,0.12)', display: 'flex', alignItems: 'center', padding: '0 36px', gap: 30, fontFamily: BODY,
      transform: `translateY(${(1 - eOut(prog(t, E.timer[0] - 0.1, E.timer[0] + 0.2))) * 80}px)`, opacity: eOut(prog(t, E.timer[0] - 0.1, E.timer[0] + 0.2))}}>
      <svg width="130" height="130" viewBox="0 0 130 130">
        <circle cx="65" cy="65" r="54" stroke="#eef0f3" strokeWidth="12" fill="none" />
        <circle cx="65" cy="65" r="54" stroke={ok ? GREEN : OR} strokeWidth="12" fill="none" strokeLinecap="round" strokeDasharray={2 * Math.PI * 54}
          strokeDashoffset={2 * Math.PI * 54 * (1 - (ok ? 1 : tk))} transform="rotate(-90 65 65)" />
        {ok ? <g transform={`translate(65 65) scale(${okK}) translate(-24 -24)`}><svg width="48" height="48" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke={GREEN} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" /></svg></g>
          : <g transform="translate(41 41)"><svg width="48" height="48" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke={OR} strokeWidth="2.2" /><path d={`M12 12L${12 + 6 * Math.sin(tk * 12.6)} ${12 - 6 * Math.cos(tk * 12.6)}`} stroke={OR} strokeWidth="2.2" strokeLinecap="round" /></svg></g>}
      </svg>
      <div>
        <Txt size={42} weight={800} color={ok ? GREEN : INK}>{ok ? 'Disponibilité confirmée !' : 'Le propriétaire vérifie…'}</Txt>
        <div style={{fontSize: 32, color: MUT, marginTop: 6}}>{ok ? 'Vous pouvez réserver' : '10 minutes maximum'}</div>
      </div>
    </div>}
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 6. acompte
const Pay: React.FC = () => {
  const t = useT(); if (!inScene(t, 'pay')) return null;
  const inK = eOut(prog(t, SC.pay[0] - 0.15, SC.pay[0] + 0.25)); const o = outK(t, 'pay');
  const ck = prog(t, E.countStart, E.countEnd); const amount = t >= E.countEnd ? 36000 : Math.floor(36000 * Math.pow(ck, 1.6));
  const sel = t >= E.select; const paid = t >= E.kaching; const pk = eBack(prog(t, E.kaching, E.kaching + 0.3));
  const fmt = (n: number) => n.toLocaleString('fr-FR').replace(/ | /g, ' ');
  return <AbsoluteFill style={{opacity: (1 - o) * inK, transform: `translateX(${(1 - inK) * 300}px)`}}>
    <CreamBG />
    <Heading t0={SC.pay[0]} title="Acompte sécurisé" sub="30 % pour réserver" y={240} />
    <div style={{position: 'absolute', left: CX - 420, top: 510, width: 840, padding: 40, borderRadius: 44, background: '#fff', boxShadow: '0 24px 60px rgba(31,36,48,0.15)', fontFamily: BODY}}>
      <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 32, color: MUT}}><span>Séjour Abidjan Classique</span><span>3 nuits</span></div>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: 10}}>
        <Txt size={40} weight={700}>Total</Txt><Txt size={44} weight={800}>120 000 FCFA</Txt></div>
      <div style={{marginTop: 30, height: 30, borderRadius: 15, background: '#f1f2f4', overflow: 'hidden'}}>
        <div style={{width: `${30 * Math.min(1, amount / 36000)}%`, height: '100%', borderRadius: 15, background: `linear-gradient(90deg, ${OR}, ${OR2})`}} /></div>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: 18}}>
        <Txt size={40} weight={700} color={OR}>Acompte 30 %</Txt>
        <Txt size={64} weight={900} color={OR} style={{transform: `scale(${t >= E.countEnd ? 1 + 0.15 * Math.exp(-(t - E.countEnd) * 10) : 1})`}}>{fmt(amount)} FCFA</Txt></div>
      {[['mobile', 'Mobile Money'], ['wallet', 'Portefeuille ResyFlex']].map(([ic, lab], i) => {
        const k = eBack(prog(t, E.methods[i], E.methods[i] + 0.3)); const on = sel && i === 0;
        return <div key={lab} style={{marginTop: i === 0 ? 34 : 18, height: 110, borderRadius: 30, border: `4px solid ${on ? OR : '#e5e7eb'}`, background: on ? '#fff4e8' : '#fff',
          display: 'flex', alignItems: 'center', gap: 22, padding: '0 30px', transform: `scale(${k})`, opacity: clamp(k * 2)}}>
          <Icon name={ic} size={50} color={on ? OR : INK} /><Txt size={40} weight={700} font={BODY}>{lab}</Txt>
          <div style={{marginLeft: 'auto', width: 44, height: 44, borderRadius: 22, border: `4px solid ${on ? OR : '#cbd0d8'}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            {on && <div style={{width: 22, height: 22, borderRadius: 11, background: OR}} />}</div>
        </div>;
      })}
      <div style={{marginTop: 30, height: 100, borderRadius: 50, background: paid ? GREEN : INK, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14,
        transform: `scale(${paid ? 0.9 + 0.1 * pk : 1})`}}>
        {paid && <Icon name="check" size={44} color="#fff" stroke={3} />}<Txt size={42} weight={700} color="#fff" font={BODY}>{paid ? 'Acompte payé' : 'Payer l’acompte'}</Txt></div>
    </div>
    <Center y={1340}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, opacity: eOut(prog(t, E.lock, E.lock + 0.3)), transform: `translateY(${(1 - eOut(prog(t, E.lock, E.lock + 0.3))) * 30}px)`}}>
        <Icon name="lock" size={44} color={OR} /><Txt size={36} weight={600} font={BODY}>Conservé par ResyFlex jusqu’à votre arrivée</Txt></div>
      <Txt size={46} weight={800} style={{marginTop: 22, opacity: eOut(prog(t, E.rest, E.rest + 0.3)), transform: `scale(${0.8 + 0.2 * eBack(prog(t, E.rest, E.rest + 0.3))})`}}>Le reste se règle à l’arrivée</Txt>
    </Center>
    <div style={{position: 'absolute', left: CX + 300, top: 490, fontFamily: BODY, fontSize: 26, color: MUT, background: '#fff', padding: '6px 16px', borderRadius: 14, boxShadow: '0 4px 12px rgba(0,0,0,0.08)'}}>Exemple</div>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 7. QR code
const QRGrid: React.FC<{t: number}> = ({t}) => {
  const N = 21; let s = 7; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  const cells: React.ReactNode[] = [];
  const finder = (r: number, c: number) => { for (const [fr, fc] of [[0, 0], [0, N - 7], [N - 7, 0]]) { const rr = r - fr, cc = c - fc; if (rr >= 0 && rr < 7 && cc >= 0 && cc < 7) return (rr === 0 || rr === 6 || cc === 0 || cc === 6 || (rr >= 2 && rr <= 4 && cc >= 2 && cc <= 4)) ? 1 : 0; } return -1; };
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) {
    const f = finder(r, c); const on = f === -1 ? rnd() > 0.5 : f === 1; const appear = E.qrBuild[0] + rnd() * (E.qrBuild[1] - E.qrBuild[0]);
    if (!on) continue; const k = eBack(prog(t, appear, appear + 0.15));
    cells.push(<rect key={r * N + c} x={c * 20 + 10 * (1 - k)} y={r * 20 + 10 * (1 - k)} width={20 * k} height={20 * k} rx={3} fill={INK} />);
  }
  return <svg width={420} height={420} viewBox="0 0 420 420">{cells}</svg>;
};
const QR: React.FC = () => {
  const t = useT(); if (!inScene(t, 'qr')) return null;
  const o = outK(t, 'qr'); const ok = t >= E.scanOk; const sk = prog(t, E.scan[0], E.scan[1]);
  const wk = eBack(prog(t, E.welcome, E.welcome + 0.35));
  return <AbsoluteFill style={{opacity: 1 - o, transform: `scale(${1 - 0.06 * o})`}}>
    <CreamBG />
    <Heading t0={SC.qr[0] + 0.6} title="Arrivée validée" sub="par QR Code" y={240} />
    <div style={{position: 'absolute', left: CX - 300, top: 520, width: 600, height: 700, borderRadius: 48, background: '#fff', boxShadow: '0 26px 60px rgba(31,36,48,0.18)',
      display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 50, fontFamily: BODY, border: `6px solid ${ok ? GREEN : '#fff'}`}}>
      <div style={{position: 'relative', width: 420, height: 420}}>
        <QRGrid t={t} />
        {sk > 0 && sk < 1 && <div style={{position: 'absolute', left: -20, right: -20, top: 420 * sk - 4, height: 8, borderRadius: 4, background: OR, boxShadow: `0 0 30px 10px rgba(245,144,30,0.55)`}} />}
        {ok && <div style={{position: 'absolute', inset: 0, background: 'rgba(22,163,74,0.12)', borderRadius: 10}} />}
      </div>
      <Txt size={40} weight={700} font={BODY} color={ok ? GREEN : INK} style={{marginTop: 40}}>{ok ? 'Réservation validée' : 'Votre QR Code'}</Txt>
      <div style={{fontSize: 30, color: MUT, marginTop: 8}}>Scanné par le propriétaire</div>
    </div>
    <Center y={1300} style={{transform: `scale(${wk})`, opacity: clamp(wk * 2)}}>
      <Txt size={64} weight={900} color={OR}>Bienvenue !</Txt>
      <Txt size={42} weight={600} font={BODY} style={{marginTop: 10}}>Votre séjour commence</Txt>
    </Center>
    {t > E.welcome && Array.from({length: 26}).map((_, i) => {
      const k = prog(t, E.welcome + (i % 6) * 0.04, E.welcome + 0.9 + (i % 6) * 0.04); if (k <= 0 || k >= 1) return null;
      const a = (i / 26) * Math.PI * 2, d = 200 + 260 * eOut(k);
      return <div key={i} style={{position: 'absolute', left: CX + Math.cos(a) * d * 1.2, top: 870 + Math.sin(a) * d, width: 18, height: 18, borderRadius: i % 3 ? 9 : 3,
        background: [OR, GREEN, '#ffd166', INK][i % 4], opacity: 1 - k, transform: `rotate(${k * 360}deg)`}} />;
    })}
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 8. engagements
const TRUST = [
  ['shield', 'Résidences vérifiées', 'contrôle sur place'],
  ['lock', 'Acompte protégé', 'jusqu’à votre arrivée'],
  ['refresh', 'Remboursement intégral', 'plus de 48 h avant l’arrivée'],
  ['star', 'Avis authentiques', 'de voyageurs ayant séjourné'],
];
const Trust: React.FC = () => {
  const t = useT(); if (!inScene(t, 'trust')) return null;
  const o = outK(t, 'trust');
  return <AbsoluteFill style={{opacity: 1 - o}}>
    <CreamBG />
    <Heading t0={SC.trust[0]} title="Nos engagements" y={260} />
    {TRUST.map(([ic, tt, sub], i) => {
      const t0 = E.trust[i]; const k = eBack(prog(t, t0, t0 + 0.35)); const x = (i % 2) * 440, y = Math.floor(i / 2) * 470;
      return <div key={tt} style={{position: 'absolute', left: CX - 430 + x, top: 470 + y, width: 420, height: 440, borderRadius: 40, background: '#fff', padding: 34,
        boxShadow: '0 20px 50px rgba(31,36,48,0.12)', transform: `scale(${k}) translateY(${(1 - k) * 60}px)`, opacity: clamp(k * 2), fontFamily: BODY}}>
        <div style={{width: 110, height: 110, borderRadius: 32, background: '#fff1e1', display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon name={ic} size={64} color={OR} stroke={2.4} /></div>
        <Txt size={42} weight={800} style={{marginTop: 30}}>{tt}</Txt>
        <div style={{fontSize: 32, color: MUT, marginTop: 12, lineHeight: 1.25}}>{sub}</div>
      </div>;
    })}
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 9. propriétaires
const Owner: React.FC = () => {
  const t = useT(); if (!inScene(t, 'owner')) return null;
  const k = eOut(prog(t, SC.owner[0] - 0.2, SC.owner[0] + 0.15)); const fk = eBack(prog(t, E.ownerFree, E.ownerFree + 0.3)); const o = outK(t, 'owner', 0.15);
  return <AbsoluteFill style={{clipPath: `circle(${k * 150}% at ${CX}px 960px)`, opacity: 1 - o}}>
    <AbsoluteFill style={{background: `linear-gradient(160deg, ${OR} 0%, ${OR2} 100%)`}} />
    <Center y={560}>
      <div style={{width: 180, height: 180, borderRadius: 50, background: 'rgba(255,255,255,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${eBack(prog(t, SC.owner[0], SC.owner[0] + 0.35))})`}}>
        <Icon name="home" size={110} color="#fff" stroke={2.2} /></div>
      <Txt size={84} weight={900} color="#fff" style={{marginTop: 40}}>Propriétaire ?</Txt>
      <Txt size={52} weight={700} color="#fff" style={{marginTop: 14}}>Publiez votre résidence</Txt>
      <div style={{marginTop: 50, padding: '22px 46px', borderRadius: 60, background: '#fff', transform: `scale(${fk})`, opacity: clamp(fk * 2), boxShadow: '0 16px 40px rgba(0,0,0,0.18)'}}>
        <Txt size={48} weight={800} color={OR}>Inscription gratuite</Txt></div>
    </Center>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 10. appel à l'action
const CTA: React.FC = () => {
  const t = useT(); if (!inScene(t, 'cta')) return null;
  const s = springAt(t, E.ctaHit, {damping: 10, stiffness: 160, mass: 0.9}); const flash = 1 - prog(t, E.ctaHit, E.ctaHit + 0.3);
  const tag = eOut(prog(t, E.ctaTag, E.ctaTag + 0.35)); const url = eBack(prog(t, E.ctaUrl, E.ctaUrl + 0.35)); const ph = eBack(prog(t, E.ctaPhone, E.ctaPhone + 0.35));
  const rings = [0, 0.07, 0.14].map((d, i) => { const k = prog(t, E.ctaHit + d, E.ctaHit + d + 0.8); if (k <= 0 || k >= 1) return null;
    return <div key={i} style={{position: 'absolute', left: CX - 700 * eOut(k), top: 760 - 700 * eOut(k), width: 1400 * eOut(k), height: 1400 * eOut(k), borderRadius: '50%', border: `${16 * (1 - k)}px solid ${i === 1 ? '#ffd166' : OR}`, opacity: 1 - k}} />; });
  return <AbsoluteFill>
    <CreamBG />{rings}
    <div style={{position: 'absolute', left: CX - 450, top: 620, width: 900, transform: `scale(${0.4 + 0.6 * s})`}}><Img src={staticFile('img/logo-full.png')} style={{width: 900}} /></div>
    <Center y={900}>
      <Txt size={50} weight={800} style={{opacity: tag, transform: `translateY(${(1 - tag) * 30}px)`}}>Trouvez · Réservez · <span style={{color: OR}}>Séjournez</span></Txt>
      <div style={{marginTop: 60, padding: '26px 60px', borderRadius: 70, background: `linear-gradient(90deg, ${OR}, ${OR2})`, transform: `scale(${url})`, opacity: clamp(url * 2), boxShadow: '0 20px 50px rgba(245,144,30,0.45)'}}>
        <Txt size={68} weight={800} color="#fff">resy-flex.com</Txt></div>
      <div style={{marginTop: 46, display: 'flex', alignItems: 'center', gap: 16, transform: `scale(${ph})`, opacity: clamp(ph * 2)}}>
        <Icon name="phone" size={50} color={OR} stroke={2.4} /><Txt size={48} weight={700} font={BODY}>+225 01 01 01 46 04</Txt></div>
    </Center>
    <AbsoluteFill style={{background: '#fff', opacity: flash * 0.85}} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ composition
export const ResyFlex: React.FC = () => {
  const t = useT();
  const fade = prog(t, E.fadeOut, TL.duration);
  return <AbsoluteFill style={{background: CREAM}}>
    <Audio src={staticFile('audio/mix.wav')} />
    <Hook /><Logo /><Find /><Verify /><Avail /><Pay /><QR /><Trust /><Owner /><CTA />
    <Chapter t0={E.chapter.find} num="01" word="TROUVEZ" />
    <Chapter t0={E.chapter.avail} num="02" word="RÉSERVEZ" />
    <Chapter t0={E.chapter.qr} num="03" word="SÉJOURNEZ" />
    <AbsoluteFill style={{background: '#000', opacity: fade}} />
  </AbsoluteFill>;
};
