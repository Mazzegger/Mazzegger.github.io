import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile} from 'remotion';
import TL from './timeline.json';
import {Logo3D, Map3D, Carousel3D, MAP_CAM, PILLAR_H, project} from './three3d';
import CIV from './civ3d.json';
import {OR, OR2, GOLD, INK, CREAM, GREEN, WHITE, HEAD, BODY, CX, clamp, prog, eOut, eOut5, eIn, eInOut, eBack, sp, useT, rng,
  Icon, Kinetic, Line, Box, DarkBG, KenBurns, Grain, LightLeaks, Flare, Flash, Ring, Particles, Phone3D, QR} from './kit';

const E: any = TL.ev, SC: any = TL.scenes, M: any = TL.music;
const BEAT = 60 / TL.bpm;
const on = (t: number, k: string, pre = 0, post = 0) => t >= SC[k][0] - pre && t < SC[k][1] + post;
const HITS: [number, number][] = [[E.slam, 42], ...E.lock.map((x: number) => [x, 8] as [number, number]), [E.cutBeats[0], 10], [E.cutBeats[2], 10], [E.cutBeats[4], 12],
  [E.mapRise, 14], [E.mapCount, 10], [E.carStamp, 24], ...E.heart.map((x: number) => [x, 10] as [number, number]), [E.confirmed, 34], [E.payNum, 22], [E.scanOk, 12],
  ...E.trust.map((x: number) => [x, 9] as [number, number]), [E.outroBurst, 14], [E.outroSlam, 40]];

// ------------------------------------------------------------------ caméra 2D : pulsation sur les temps (sauf pendant le break) + secousses
const Camera: React.FC<{children: React.ReactNode}> = ({children}) => {
  const t = useT();
  let shake = 0; for (const [h, a] of HITS) if (t >= h) shake += a * Math.exp(-(t - h) * 9);
  const r = rng(Math.floor(t * 60) + 7);
  const inBreak = t >= SC.brk[0] && t < M.drop2;
  const beat = t >= M.drop1 && !inBreak && t < E.fade ? ((t - M.drop1) % BEAT) : 9;
  const pulse = 0.016 * Math.exp(-beat * 11);
  return <AbsoluteFill style={{transform: `translate(${(r() - 0.5) * shake}px, ${(r() - 0.5) * shake}px) scale(${1 + pulse}) rotate(${(r() - 0.5) * shake * 0.03}deg)`}}>{children}</AbsoluteFill>;
};

// ------------------------------------------------------------------ 1. intro + héros : le symbole ResyFlex en 3D
const Hero: React.FC = () => {
  const t = useT(); if (t >= SC.hero[1] + 0.05) return null;
  const out = eIn(prog(t, E.heroOut, SC.hero[1]));
  const wm = eOut5(prog(t, E.wordmark, E.wordmark + 0.6));
  const txtOut = prog(t, E.slam - 0.35, E.slam - 0.1);
  return <AbsoluteFill style={{transform: `scale(${1 + out * 2.2})`, filter: `blur(${out * 16}px)`, opacity: 1 - prog(t, SC.hero[1] - 0.06, SC.hero[1] + 0.04)}}>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, #2a1606 0%, #0b0b10 55%, #050507 100%)'}} />
    <Logo3D t={t} mode="intro" ev={E} y={1.3} />
    {/* phrases d'accroche pendant l'assemblage */}
    <div style={{opacity: 1 - txtOut}}>
      <Box y={1330}><Kinetic text="Votre prochain séjour" t0={E.introText[0]} size={78} stagger={0.02} /></Box>
      <Box y={1440}><Kinetic text="commence ici." t0={E.introText[1]} size={78} color={OR} stagger={0.03} /></Box>
    </div>
    {/* nom (découpé du fichier officiel du logo) + accroche sous le symbole 3D */}
    {t >= E.wordmark && <div style={{position: 'absolute', left: CX - 380, top: 1080, width: 760, clipPath: `inset(0 ${(1 - wm) * 100}% 0 0)`, transform: `translateY(${(1 - wm) * 30}px)`}}>
      <div style={{background: CREAM, borderRadius: 28, padding: '18px 34px', boxShadow: '0 20px 60px rgba(245,144,30,0.35)'}}>
        <Img src={staticFile('img/wordmark.png')} style={{width: '100%', display: 'block'}} />
      </div>
    </div>}
    <Box y={1395}><Line t0={E.slogan} size={44} color={WHITE} weight={700}>Résidences meublées en Côte d’Ivoire</Line></Box>
    <Flash t0={E.slam} d={0.22} a={0.85} />
    <Flare t0={E.slam + 0.03} y={750} />
    <Ring t0={E.slam} y={750} r={950} /><Ring t0={E.slam + 0.07} y={750} r={700} c={GOLD} w={10} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 2. rafale sur le temps : vraies photos + promesse
const CUTS: [string, string, string?][] = [['abidjan', 'TROUVEZ'], ['korhogo', '', 'Korhogo'], ['walebo', 'RÉSERVEZ'], ['sanpedro', '', 'San-Pedro'],
  ['vip', 'SÉJOURNEZ'], ['grandlahou', '', 'Grand-Lahou'], ['', 'Liberté,'], ['', 'Confort et Sérénité']];
const Cuts: React.FC = () => {
  const t = useT(); if (!on(t, 'cuts')) return null;
  const i = Math.min(7, E.cutBeats.filter((x: number) => t >= x).length - 1); const [img, word, city] = CUTS[i]; const t0 = E.cutBeats[i];
  const dir = i % 2 ? 1 : -1; const k = eOut5(prog(t, t0, t0 + 0.2));
  return <AbsoluteFill style={{background: INK}}>
    {img ? <AbsoluteFill style={{transform: `translateX(${(1 - k) * dir * 300}px)`}}>
      <KenBurns src={img} t0={t0} dur={0.5} from={1.3} to={1.12} dx={dir * 30} />
      <AbsoluteFill style={{background: word ? 'rgba(11,13,18,0.45)' : 'linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.7))'}} />
    </AbsoluteFill> : <DarkBG />}
    {word && <Box y={i >= 6 ? (i === 6 ? 760 : 760) : 840}><Kinetic text={word} t0={t0} size={i === 7 ? 96 : word.length > 8 ? 140 : 160} color={i >= 6 ? (i === 6 ? WHITE : OR) : WHITE} stagger={0.016} /></Box>}
    {i === 7 && <Box y={650}><Kinetic text="Liberté," t0={E.cutBeats[6]} size={120} stagger={0} /></Box>}
    {city && <div style={{position: 'absolute', left: 70, top: 1330, display: 'flex', alignItems: 'center', gap: 14, padding: '16px 28px', borderRadius: 50, background: 'rgba(255,255,255,0.95)',
      transform: `translateY(${(1 - k) * 40}px)`, opacity: k}}><Icon n="pin" s={40} c={OR} w={2.6} /><span style={{fontFamily: HEAD, fontWeight: 800, fontSize: 44, color: INK}}>{city}</span></div>}
    <Flash t0={t0} d={0.1} a={0.5} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 3. carte 3D
const ORDER = ['Abidjan', 'San-Pedro', 'Korhogo', 'Grand-Bassam', 'Bingerville', 'Boundiali', 'Grand-Lahou'];
const LBL: Record<string, [number, number]> = {'Abidjan': [-130, -70], 'Bingerville': [20, -75], 'Grand-Bassam': [40, 10], 'San-Pedro': [-70, 10], 'Korhogo': [20, -30], 'Boundiali': [-170, -30], 'Grand-Lahou': [-100, 115]};
const MapScene: React.FC = () => {
  const t = useT(); if (!on(t, 'map')) return null;
  const {pos, look} = MAP_CAM(t, E);
  const cnt = ORDER.filter((_, i) => t >= E.pillars[i]).length;
  const out = eIn(prog(t, SC.map[1] - 0.25, SC.map[1]));
  return <AbsoluteFill style={{opacity: 1 - out, transform: `scale(${1 + out * 0.3})`}}>
    <DarkBG hue={GOLD} />
    <Map3D t={t} ev={E} order={ORDER} />
    {ORDER.map((c, i) => {
      if (t < E.pillars[i]) return null; const [x, y] = (CIV.cities as any)[c];
      const [px, py] = project([x, 0.42 + PILLAR_H + 0.25, -y], pos, look, 32); const k = eOut5(prog(t, E.pillars[i] + 0.1, E.pillars[i] + 0.45)); const [dx, dy] = LBL[c];
      return <div key={c} style={{position: 'absolute', left: px + dx, top: py + dy - 20, opacity: k, transform: `translateY(${(1 - k) * 20}px)`, fontFamily: BODY, fontWeight: 800, fontSize: 36, color: WHITE,
        textShadow: '0 3px 12px rgba(0,0,0,0.9)', whiteSpace: 'nowrap'}}>{c}</div>;
    })}
    <Box y={250} style={{opacity: cnt > 0 ? 1 : 0}}>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 22}}>
        <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 200, color: OR, lineHeight: 1, transform: `scale(${t >= E.mapCount ? 1 + 0.22 * Math.exp(-(t - E.mapCount) * 9) : 1})`}}>{cnt}</div>
        <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 92, color: WHITE, lineHeight: 1}}>{cnt > 1 ? 'villes' : 'ville'}</div>
      </div>
      <Line t0={E.mapCount} size={44} color={GOLD} weight={700}>déjà disponibles</Line>
    </Box>
    <Box y={1420}><Line t0={E.mapCount + 0.1} size={36} color="rgba(255,255,255,0.85)">et bientôt Yamoussoukro, Bouaké, Assinie…</Line></Box>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 4. carrousel 3D
const PHOTOS = ['abidjan', 'walebo', 'vip', 'korhogo', 'sanpedro', 'grandlahou', 'abidjan104', 'angre'];
const Carousel: React.FC = () => {
  const t = useT(); if (!on(t, 'carousel')) return null;
  const st = prog(t, E.carStamp - 0.1, E.carStamp); const out = eIn(prog(t, SC.carousel[1] - 0.2, SC.carousel[1]));
  return <AbsoluteFill style={{opacity: 1 - out}}>
    <DarkBG />
    <Carousel3D t={t} ev={E} photos={PHOTOS} />
    <Box y={240}><Kinetic text="Des résidences" t0={SC.carousel[0] + 0.1} size={84} stagger={0.018} /></Box>
    <Box y={340}><Kinetic text="vérifiées sur place" t0={SC.carousel[0] + 0.3} size={64} color={OR} weight={800} stagger={0.015} /></Box>
    {st > 0 && <div style={{position: 'absolute', left: CX - 430, top: 1250, width: 860, display: 'flex', justifyContent: 'center', transform: `scale(${3 - 2 * eOut(st)}) rotate(-6deg)`, opacity: clamp(st * 1.5)}}>
      <div style={{padding: '18px 40px', border: `10px solid ${GREEN}`, borderRadius: 30, background: 'rgba(255,255,255,0.96)', display: 'flex', alignItems: 'center', gap: 18, boxShadow: '0 20px 60px rgba(22,163,74,0.5)'}}>
        <Icon n="shield" s={84} c={GREEN} w={2.6} />
        <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 80, color: GREEN, lineHeight: 1}}>100 %<br /><span style={{fontSize: 58}}>VÉRIFIÉES</span></div>
      </div>
    </div>}
    <Box y={1480}><Line t0={E.carSub} size={38} weight={700}>Contrôle complet sur place</Line></Box>
    <Particles t0={E.carStamp} y={1340} n={30} colors={[GREEN, WHITE, GOLD]} dist={560} seed={9} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 5. break : suspense 10 MIN, puis second drop
const Break: React.FC = () => {
  const t = useT(); if (!on(t, 'brk', 0, 0.46)) return null;
  const tk = eInOut(prog(t, E.tick[0], E.tick[1])); const hb = E.heart.reduce((a: number, h: number) => a + (t >= h ? Math.exp(-(t - h) * 6) : 0), 0);
  const sil = t >= E.silence[0] && t < E.confirmed; const conf = t >= E.confirmed; const nk = eBack(prog(t, E.confirmed, E.confirmed + 0.35));
  const s10 = sp(t, SC.brk[0] + 0.05, 10, 160); const R = 350;
  return <AbsoluteFill style={{background: '#050507'}}>
    <AbsoluteFill style={{background: `radial-gradient(circle at ${CX}px 900px, rgba(245,144,30,${0.18 + 0.35 * hb}) 0%, transparent ${45 + 10 * hb}%)`, opacity: sil ? 0.2 : 1}} />
    <Box y={250} style={{opacity: conf ? 0 : 1}}><Kinetic text="Le propriétaire confirme…" t0={SC.brk[0] + 0.1} size={60} color={WHITE} weight={800} stagger={0.014} /></Box>
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, opacity: sil ? 0.35 : 1, transform: `scale(${1 + 0.04 * hb})`, transformOrigin: `${CX}px 900px`}}>
      <g transform={`translate(${CX} 900)`}>
        {Array.from({length: 60}).map((_, i) => {
          const a = (i / 60) * Math.PI * 2 - Math.PI / 2, lit = conf || i / 60 <= tk, L = i % 5 === 0 ? 34 : 16;
          return <line key={i} x1={Math.cos(a) * (R - L)} y1={Math.sin(a) * (R - L)} x2={Math.cos(a) * R} y2={Math.sin(a) * R} stroke={lit ? (conf ? GREEN : OR) : 'rgba(255,255,255,0.15)'} strokeWidth={i % 5 === 0 ? 7 : 4} strokeLinecap="round" />;
        })}
      </g>
    </svg>
    <div style={{position: 'absolute', left: CX - 400, top: 650, width: 800, display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 10, transform: `scale(${(0.3 + 0.7 * s10) * (1 + 0.05 * hb)})`, opacity: sil ? 0.4 : 1}}>
      <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 330, color: conf ? GREEN : WHITE, lineHeight: 1}}>10</div>
      <div style={{fontFamily: HEAD, fontWeight: 900, fontSize: 116, color: conf ? GREEN : OR, lineHeight: 1}}>MIN</div>
    </div>
    <Box y={1300} style={{opacity: conf ? 0 : 1}}><Line t0={SC.brk[0] + 0.3} size={44} weight={700}>10 minutes maximum</Line></Box>
    {conf && <div style={{position: 'absolute', left: CX - 430, top: 1260, width: 860, padding: '28px 30px', borderRadius: 36, background: 'rgba(255,255,255,0.97)', transform: `scale(${nk})`,
      boxShadow: '0 30px 70px rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', gap: 22, fontFamily: BODY}}>
      <div style={{width: 88, height: 88, borderRadius: 26, background: GREEN, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon n="check" s={56} c={WHITE} w={3} /></div>
      <div><div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 44, color: INK}}>Disponibilité confirmée</div><div style={{fontSize: 32, color: '#6b7280'}}>Vous pouvez réserver</div></div>
    </div>}
    <Flash t0={E.confirmed} d={0.25} a={0.9} /><Ring t0={E.confirmed} y={900} r={900} c={GREEN} /><Flare t0={E.confirmed} y={900} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 6. 30 %
const Pay: React.FC = () => {
  const t = useT(); if (!(t >= E.confirmed + 0.35 && t < SC.pay[1] + 0.25)) return null;
  const inK = eOut5(prog(t, E.confirmed + 0.35, E.payNum)); const out = eIn(prog(t, SC.pay[1] - 0.2, SC.pay[1] + 0.05));
  const fill = eInOut(prog(t, E.fill[0], E.fill[1])); const s = sp(t, E.payNum, 9, 210);
  return <AbsoluteFill style={{clipPath: `circle(${inK * 150}% at ${CX}px 960px)`, transform: `translateX(${out * 1300}px)`, filter: `blur(${out * 20}px)`}}>
    <AbsoluteFill style={{background: `linear-gradient(160deg, ${OR} 0%, ${OR2} 100%)`}} />
    <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 35%, rgba(255,255,255,0.25), transparent 55%)'}} />
    <div style={{position: 'absolute', left: CX - 470, top: 380, width: 940, height: 420, transform: `scale(${0.3 + 0.7 * s})`}}>
      <div style={{position: 'absolute', inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', fontFamily: HEAD, fontWeight: 900, fontSize: 340, lineHeight: 1, color: 'transparent', WebkitTextStroke: '6px #fff', letterSpacing: -10}}>30 %</div>
      <div style={{position: 'absolute', inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', fontFamily: HEAD, fontWeight: 900, fontSize: 340, lineHeight: 1, color: '#fff', letterSpacing: -10, clipPath: `inset(${(1 - fill) * 100}% 0 0 0)`}}>30 %</div>
    </div>
    <Box y={860}><Kinetic text="d’acompte sécurisé" t0={E.fill[1] - 0.2} size={76} stagger={0.018} /></Box>
    {[['mobile', 'Mobile Money'], ['wallet', 'Portefeuille ResyFlex']].map(([ic, lab], i) => {
      const k = eBack(prog(t, E.chips[i], E.chips[i] + 0.35)); if (t < E.chips[i]) return null;
      return <div key={lab} style={{position: 'absolute', left: CX - 360, top: 1030 + i * 140, width: 720, height: 116, borderRadius: 60, background: INK, display: 'flex', alignItems: 'center', gap: 22, padding: '0 34px', transform: `scale(${k})`, opacity: clamp(k * 2)}}>
        <div style={{width: 70, height: 70, borderRadius: 35, background: OR, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon n={ic} s={40} c={WHITE} w={2.4} /></div>
        <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 42, color: WHITE}}>{lab}</span></div>;
    })}
    <Box y={1340}><Line t0={E.rest} size={50} color={INK} weight={800} font={HEAD}>Le reste se règle à l’arrivée</Line></Box>
    <Particles t0={E.coins} y={1200} n={34} colors={[GOLD, '#fff3c4', '#e0a020']} dist={560} seed={21} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 7. QR Code
const Stay: React.FC = () => {
  const t = useT(); if (!on(t, 'qr', 0, 0.25)) return null;
  const inK = eOut5(prog(t, SC.qr[0], SC.qr[0] + 0.6)); const out = eIn(prog(t, SC.qr[1] - 0.25, SC.qr[1] + 0.1));
  const ok = t >= E.scanOk; const sk = prog(t, E.scan[0], E.scan[1]); const rays = eOut(prog(t, E.welcome, E.welcome + 0.8));
  return <AbsoluteFill style={{transform: `scale(${1 + out * 3})`, filter: `blur(${out * 20}px)`, opacity: 1 - prog(t, SC.qr[1], SC.qr[1] + 0.2)}}>
    <DarkBG hue={ok ? GREEN : OR} />
    {rays > 0 && <AbsoluteFill style={{background: `conic-gradient(from ${t * 20}deg at ${CX}px 1000px, ${Array.from({length: 12}, (_, i) => `rgba(255,200,110,${i % 2 ? 0 : 0.22 * rays}) ${i * 30}deg ${(i + 1) * 30}deg`).join(',')})`, mixBlendMode: 'screen'}} />}
    <Box y={240}><Kinetic text="Arrivée validée" t0={SC.qr[0] + 0.1} size={80} stagger={0.02} /></Box>
    <Box y={340}><Kinetic text="par QR Code" t0={SC.qr[0] + 0.3} size={60} color={OR} weight={800} stagger={0.02} /></Box>
    <Phone3D x={CX} y={1010 + (1 - inK) * 700} w={430} ry={(1 - inK) * 40 + 6 * Math.sin((t - SC.qr[0]) * 1.1)} rx={(1 - inK) * 10}>
      <AbsoluteFill style={{background: ok ? '#ecfdf3' : WHITE, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 150, fontFamily: BODY}}>
        <Img src={staticFile('img/logo-full.png')} style={{width: 230}} />
        <div style={{marginTop: 50, position: 'relative', padding: 18, borderRadius: 24, border: `6px solid ${ok ? GREEN : '#e5e7eb'}`, background: WHITE}}>
          <QR t={t} build={E.qrBuild} />
          {sk > 0 && sk < 1 && <div style={{position: 'absolute', left: -10, right: -10, top: 18 + 294 * sk - 3, height: 6, background: OR, boxShadow: '0 0 26px 8px rgba(245,144,30,0.7)', borderRadius: 3}} />}
        </div>
        <div style={{marginTop: 40, fontFamily: HEAD, fontWeight: 800, fontSize: 34, color: ok ? GREEN : INK}}>{ok ? 'Réservation validée ✓' : 'Votre QR Code'}</div>
      </AbsoluteFill>
    </Phone3D>
    {t >= E.welcome && <Box y={1470} style={{zIndex: 10}}><Kinetic text="Bienvenue chez vous" t0={E.welcome} size={66} color={GOLD} stagger={0.018} /></Box>}
    <Ring t0={E.scanOk} y={1000} r={700} c={GREEN} />
    <Particles t0={E.scanOk} y={1000} n={36} colors={[GREEN, GOLD, WHITE]} dist={560} seed={33} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 8. engagements
const TRUST: [string, string, string, string][] = [['shield', 'Vérifiées', 'sur place', OR], ['lock', 'Acompte', 'protégé', INK], ['refresh', 'Remboursé', 'jusqu’à 48 h avant', CREAM], ['star', 'Avis', 'authentiques', OR]];
const Trust: React.FC = () => {
  const t = useT(); if (!on(t, 'trust')) return null;
  const i = Math.min(3, E.trust.filter((x: number) => t >= x).length - 1); const [ic, a, b, bg] = TRUST[i]; const t0 = E.trust[i];
  const fg = bg === CREAM ? INK : WHITE, ac = bg === OR ? INK : OR; const k = sp(t, t0, 10, 260);
  return <AbsoluteFill style={{background: bg}}>
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, rgba(255,255,255,${bg === INK ? 0.06 : 0.22}), transparent 60%)`}} />
    <Box y={560}>
      <div style={{width: 230, height: 230, borderRadius: 70, background: bg === OR ? INK : OR, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${k}) rotate(${(1 - k) * -25}deg)`}}><Icon n={ic} s={140} c={WHITE} w={2.2} /></div>
      <div style={{marginTop: 50, fontFamily: HEAD, fontWeight: 900, fontSize: 150, color: fg, lineHeight: 1, transform: `scale(${0.6 + 0.4 * k})`}}>{a}</div>
      <div style={{marginTop: 10, fontFamily: HEAD, fontWeight: 900, fontSize: b.length > 12 ? 68 : 104, color: ac, lineHeight: 1, transform: `translateY(${(1 - k) * 60}px)`}}>{b}</div>
    </Box>
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 9. propriétaires
const Owner: React.FC = () => {
  const t = useT(); if (!on(t, 'owner')) return null;
  const k = eOut5(prog(t, SC.owner[0], SC.owner[0] + 0.35)); const g = eBack(prog(t, E.owner[2], E.owner[2] + 0.35)); const suck = eIn(prog(t, SC.owner[1] - 0.25, SC.owner[1]));
  return <AbsoluteFill style={{clipPath: `circle(${k * 150}% at ${CX}px 960px)`, transform: `scale(${1 - suck * 0.6})`, opacity: 1 - suck}}>
    <KenBurns src="angre" t0={SC.owner[0]} dur={2} from={1.3} to={1.1} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(17,20,27,0.75), rgba(17,20,27,0.55) 50%, rgba(17,20,27,0.85))'}} />
    <Box y={560}><Kinetic text="Propriétaire ?" t0={E.owner[0] + 0.05} size={118} stagger={0.02} /></Box>
    <Box y={720}><Kinetic text="Publiez votre résidence" t0={E.owner[1]} size={64} color={GOLD} weight={800} stagger={0.015} /></Box>
    {t >= E.owner[2] && <Box y={900}><div style={{padding: '26px 56px', borderRadius: 70, background: OR, transform: `scale(${g})`, boxShadow: '0 20px 60px rgba(245,144,30,0.55)'}}>
      <span style={{fontFamily: HEAD, fontWeight: 900, fontSize: 64, color: WHITE}}>Inscription gratuite</span></div></Box>}
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ 10. outro : le symbole 3D se reforme + appel à l'action
const Outro: React.FC = () => {
  const t = useT(); if (!on(t, 'outro')) return null;
  const wm = eOut5(prog(t, E.outroSlam + 0.35, E.outroSlam + 0.9)); const u = eBack(prog(t, E.ctaUrl, E.ctaUrl + 0.4)); const ph = eOut5(prog(t, E.ctaPhone, E.ctaPhone + 0.4));
  return <AbsoluteFill>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 35%, #2a1606 0%, #0b0b10 55%, #050507 100%)'}} />
    <Logo3D t={t} mode="outro" ev={E} y={1.9} />
    {t >= E.outroSlam && <div style={{position: 'absolute', left: CX - 330, top: 950, width: 660, clipPath: `inset(0 ${(1 - wm) * 100}% 0 0)`}}>
      <div style={{background: CREAM, borderRadius: 26, padding: '16px 30px'}}><Img src={staticFile('img/wordmark.png')} style={{width: '100%', display: 'block'}} /></div></div>}
    <Box y={1200}><Kinetic text="Trouvez · Réservez · Séjournez" t0={E.ctaTag} size={52} weight={800} stagger={0.012} spacing={0} /></Box>
    {t >= E.ctaUrl && <Box y={1290}><div style={{padding: '26px 60px', borderRadius: 80, background: `linear-gradient(90deg, ${OR}, ${OR2})`, transform: `scale(${u})`, boxShadow: '0 24px 60px rgba(245,144,30,0.5)'}}>
      <span style={{fontFamily: HEAD, fontWeight: 900, fontSize: 74, color: WHITE}}>resy-flex.com</span></div></Box>}
    <Box y={1450}><div style={{display: 'flex', alignItems: 'center', gap: 16, opacity: ph, transform: `translateY(${(1 - ph) * 30}px)`}}><Icon n="phone" s={50} c={OR} w={2.4} />
      <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 48, color: WHITE}}>+225 01 01 01 46 04</span></div></Box>
    <Flash t0={E.outroSlam} d={0.25} a={0.75} /><Flare t0={E.outroSlam + 0.03} y={660} />
    <Ring t0={E.outroSlam} y={660} r={900} /><Ring t0={E.outroSlam + 0.08} y={660} r={650} c={GOLD} w={10} />
  </AbsoluteFill>;
};

// ------------------------------------------------------------------ composition
export const ResyFlex3: React.FC = () => {
  const t = useT();
  return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
    <Audio src={staticFile('audio/mix.wav')} />
    <Camera>
      <Hero /><Cuts /><MapScene /><Carousel /><Break /><Pay /><Stay /><Trust /><Owner /><Outro />
    </Camera>
    <LightLeaks hits={HITS} />
    <Grain />
    <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
    <AbsoluteFill style={{background: '#000', opacity: prog(t, E.fade, TL.duration)}} />
  </AbsoluteFill>;
};
