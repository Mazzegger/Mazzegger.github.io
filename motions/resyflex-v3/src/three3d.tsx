import React, {useMemo, useState, useEffect} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {staticFile, delayRender, continueRender, Easing} from 'remotion';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {useThree} from '@react-three/fiber';
import SHAPES from './logo_mark_shapes.json';
import CIV from './civ3d.json';

export const W = 1080, H = 1920, OR = '#f5901e';
const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
const eOut = (k: number) => Easing.out(Easing.cubic)(clamp(k));
const eOut5 = (k: number) => Easing.out(Easing.poly(5))(clamp(k));
const eIn = (k: number) => Easing.in(Easing.cubic)(clamp(k));
const eInOut = (k: number) => Easing.inOut(Easing.cubic)(clamp(k));
const eBack = (k: number) => Easing.out(Easing.back(1.6))(clamp(k));
const lerp = (a: number, b: number, k: number) => a + (b - a) * k;

// ------------------------------------------------------------------ environnement (reflets) + caméra pilotée
const Env: React.FC<{intensity?: number}> = ({intensity = 1}) => {
  const {gl, scene} = useThree();
  useMemo(() => { const pm = new THREE.PMREMGenerator(gl); scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; (scene as any).environmentIntensity = intensity; }, [gl, scene]);
  return null;
};
const Cam: React.FC<{pos: [number, number, number]; look: [number, number, number]; fov?: number}> = ({pos, look, fov = 32}) => {
  const {camera} = useThree();
  camera.position.set(...pos); (camera as THREE.PerspectiveCamera).fov = fov; (camera as THREE.PerspectiveCamera).aspect = W / H;
  (camera as THREE.PerspectiveCamera).updateProjectionMatrix(); camera.lookAt(...look);
  return null;
};
// projection d'un point 3D vers l'écran (pour poser des étiquettes 2D au bon endroit)
export const project = (p: [number, number, number], pos: [number, number, number], look: [number, number, number], fov = 32) => {
  const c = new THREE.PerspectiveCamera(fov, W / H, 0.1, 200); c.position.set(...pos); c.lookAt(...look); c.updateMatrixWorld(); c.updateProjectionMatrix();
  const v = new THREE.Vector3(...p).project(c); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H, v.z] as [number, number, number];
};

// textures avec attente du chargement
const useTextures = (urls: string[]) => {
  const [tex, setTex] = useState<THREE.Texture[] | null>(null);
  const [handle] = useState(() => delayRender('textures ' + urls.join(',')));
  useEffect(() => {
    const ld = new THREE.TextureLoader();
    Promise.all(urls.map((u) => new Promise<THREE.Texture>((res, rej) => ld.load(u, (t) => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; res(t); }, undefined, rej))))
      .then((ts) => { setTex(ts); continueRender(handle); }).catch(() => continueRender(handle));
  }, []);
  return tex;
};
// texture de dégradé radial (faisceaux, halos)
const useGlowTex = () => useMemo(() => {
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d')!;
  const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c);
}, []);
const useBeamTex = () => useMemo(() => {
  const c = document.createElement('canvas'); c.width = 64; c.height = 512; const g = c.getContext('2d')!;
  const gx = g.createLinearGradient(0, 0, 64, 0); gx.addColorStop(0, 'rgba(255,255,255,0)'); gx.addColorStop(0.5, 'rgba(255,255,255,1)'); gx.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gx; g.fillRect(0, 0, 64, 512);
  const gy = g.createLinearGradient(0, 0, 0, 512); gy.addColorStop(0, 'rgba(0,0,0,0)'); gy.addColorStop(0.25, 'rgba(0,0,0,1)'); gy.addColorStop(1, 'rgba(0,0,0,0)');
  g.globalCompositeOperation = 'destination-in'; g.fillStyle = gy; g.fillRect(0, 0, 64, 512); return new THREE.CanvasTexture(c);
}, []);

// ------------------------------------------------------------------ géométrie du symbole ResyFlex (tracé du fichier officiel, IoU 99,9 %)
const usePieceGeos = () => useMemo(() => SHAPES.pieces.map((pts: number[][]) => {
  const s = new THREE.Shape(pts.map(([x, y]) => new THREE.Vector2(x, y)));
  const g = new THREE.ExtrudeGeometry(s, {depth: 0.55, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.055, bevelSegments: 8, curveSegments: 16});
  g.translate(0, 0, -0.275); g.computeBoundingBox(); return g;
}), []);
const pieceCenters = SHAPES.pieces.map((pts: number[][]) => {
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]); return [(Math.min(...xs) + Math.max(...xs)) / 2, (Math.min(...ys) + Math.max(...ys)) / 2];
});

const Particles: React.FC<{t: number; n?: number; spread?: number; color?: string; seed?: number; speed?: number; size?: number; opacity?: number}> = ({t, n = 500, spread = 14, color = '#ffb35c', seed = 1, speed = 0.4, size = 0.05, opacity = 0.9}) => {
  const tex = useGlowTex();
  const base = useMemo(() => { let s = seed; const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647; }; return Array.from({length: n}, () => [(r() - 0.5) * spread, (r() - 0.5) * spread * 1.6, (r() - 0.5) * spread * 0.8 - 2, r()]); }, [n]);
  const geo = useMemo(() => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3)); return g; }, [n]);
  const arr = geo.attributes.position.array as Float32Array;
  base.forEach(([x, y, z, ph], i) => { arr[i * 3] = x + 0.3 * Math.sin(t * 0.7 + ph * 9); arr[i * 3 + 1] = ((y + t * speed * (0.5 + ph) + spread * 0.8) % (spread * 1.6)) - spread * 0.8; arr[i * 3 + 2] = z; });
  geo.attributes.position.needsUpdate = true;
  return <points geometry={geo}><pointsMaterial size={size} map={tex} color={color} transparent opacity={opacity} depthWrite={false} blending={THREE.AdditiveBlending} sizeAttenuation /></points>;
};

const Beams: React.FC<{t: number; strength?: number}> = ({t, strength = 1}) => {
  const tex = useBeamTex();
  return <group position={[0, 0, -6]}>
    {[0, 1, 2, 3, 4].map((i) => {
      const a = -0.9 + i * 0.45 + 0.25 * Math.sin(t * 0.6 + i * 1.7);
      return <mesh key={i} position={[(i - 2) * 1.6, 5, 0]} rotation={[0, 0, a]}>
        <planeGeometry args={[1.6 + (i % 2) * 0.8, 26]} />
        <meshBasicMaterial map={tex} color={i % 2 ? '#ff9a3c' : '#ffd29a'} transparent opacity={(0.11 + 0.05 * Math.sin(t * 1.3 + i)) * strength} blending={THREE.AdditiveBlending} depthWrite={false} />
      </mesh>;
    })}
  </group>;
};

// ------------------------------------------------------------------ LOGO 3D
type LogoProps = {t: number; mode: 'intro' | 'outro'; ev: any; y?: number};
export const Logo3D: React.FC<LogoProps> = ({t, mode, ev, y = 0}) => {
  const geos = usePieceGeos();
  const glow = useGlowTex();
  const isIntro = mode === 'intro';
  const appear: number[] = isIntro ? ev.pieces : ev.outroLock.map((x: number) => x - 0.55);
  const lock: number[] = isIntro ? ev.lock : ev.outroLock;
  const slam: number = isIntro ? ev.slam : ev.outroSlam;
  const starts = [[-7, 4, -14], [8, 6, -18], [-6, -7, -10], [7, -5, -16]];
  const spins = [[3, 5, 2], [-4, 3, -3], [5, -3, 4], [-3, -5, -2]];
  const sinceSlam = t - slam;
  // caméra : approche + orbite, coup de caméra au moment de l'assemblage
  let az: number, dist: number, el: number;
  if (isIntro) { const k = eInOut(prog(t, 0, 9.45)); az = lerp(-0.62, 0.32, k); dist = lerp(40, 22.5, eOut(prog(t, 0, 6.2))) - (t > slam ? 1.0 * eOut(prog(t, slam, slam + 3)) : 0); el = lerp(0.35, 0.12, k); }
  else { const k = eInOut(prog(t, ev.outroBurst, ev.outroBurst + 6.5)); az = lerp(0.9, -0.18, k); dist = lerp(36, 23.5, eOut(prog(t, ev.outroBurst, slam + 0.4))); el = lerp(-0.25, 0.1, k); }
  const shake = sinceSlam > 0 ? 0.35 * Math.exp(-sinceSlam * 8) : 0;
  const pos: [number, number, number] = [Math.sin(az) * dist + Math.sin(t * 90) * shake, Math.sin(el) * dist + Math.cos(t * 77) * shake, Math.cos(az) * dist];
  const flash = sinceSlam > 0 ? Math.exp(-sinceSlam * 5) : 0;
  const sweepX = isIntro ? lerp(-9, 9, eInOut(prog(t, ev.sweep, ev.sweep + 1.1))) : lerp(-9, 9, eInOut(prog(t, slam + 0.5, slam + 1.6)));
  const breathe = sinceSlam > 0 ? 1 + 0.03 * Math.exp(-sinceSlam * 6) * Math.sin(sinceSlam * 30) : 1;
  return <ThreeCanvas width={W} height={H} style={{position: 'absolute', inset: 0}} gl={{antialias: true, alpha: true, toneMapping: THREE.ACESFilmicToneMapping}}>
    <Cam pos={pos} look={[0, 0, 0]} fov={30} />
    <Env intensity={0.9} />
    <ambientLight intensity={0.15} />
    <directionalLight position={[6, 8, 10]} intensity={2.4} />
    <directionalLight position={[-8, -3, -6]} intensity={1.6} color="#ff8a2a" />
    <pointLight position={[sweepX, 3 + y, 4]} intensity={160} distance={14} color="#ffffff" />
    <pointLight position={[0, y, 3]} intensity={120 * flash} distance={10} color="#ffb060" />
    <Beams t={t} strength={isIntro ? 1 : 0.7} />
    <Particles t={t} n={isIntro ? 650 : 450} seed={isIntro ? 3 : 9} />
    <group position={[0, y, 0]} scale={breathe}>
      {geos.map((g, i) => {
        const a = prog(t, appear[i], lock[i]);
        if (t < appear[i]) return null;
        const [cx, cy] = pieceCenters[i]; const dir = new THREE.Vector2(cx, cy).normalize();
        const hover = [cx + dir.x * 1.1 - cx, cy + dir.y * 1.1 - cy, 1.8 + i * 0.25];       // écartée avant l'assemblage
        const k = eOut5(a); const st = starts[i];
        const fly = [lerp(st[0], hover[0], k), lerp(st[1], hover[1], k), lerp(st[2], hover[2], k)];
        const floatK = t > lock[i] ? Math.sin((t - lock[i]) * 2.2 + i) * 0.06 : 0;
        const j = eIn(prog(t, slam - 0.16, slam));                                          // claque en place
        const p = [lerp(fly[0], 0, j), lerp(fly[1] + floatK, 0, j), lerp(fly[2], 0, j)];
        const sp = spins[i]; const r = (1 - k) * 1;
        const lockKick = t > lock[i] && t < slam ? 0.12 * Math.exp(-(t - lock[i]) * 7) : 0;
        return <mesh key={i} geometry={g} position={p as any} rotation={[sp[0] * r * (1 - j) + lockKick, sp[1] * r * (1 - j) + 0.15 * (1 - j), sp[2] * r * (1 - j)]}>
          <meshPhysicalMaterial color={OR} metalness={0.55} roughness={0.2} clearcoat={1} clearcoatRoughness={0.06} envMapIntensity={1.1}
            emissive={'#ff7a10'} emissiveIntensity={0.05 + 1.4 * flash + (t > lock[i] && t < slam ? 0.4 * Math.exp(-(t - lock[i]) * 5) : 0)} />
        </mesh>;
      })}
      {/* halo derrière le symbole */}
      <mesh position={[0, 0, -1.2]}><planeGeometry args={[14, 14]} /><meshBasicMaterial map={glow} color="#ff8a20" transparent opacity={(t > slam - 0.2 ? 0.35 + 0.6 * flash : 0.12) } blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
    </group>
    {/* reflet au sol */}
    <group position={[0, y - 5.0, 0]} scale={[1, -1, 1]}>
      {t >= slam && geos.map((g, i) => <mesh key={i} geometry={g}>
        <meshStandardMaterial color={OR} metalness={0.4} roughness={0.4} transparent opacity={0.07} emissive="#ff7a10" emissiveIntensity={0.1 + 0.5 * flash} />
      </mesh>)}
    </group>
  </ThreeCanvas>;
};

// ------------------------------------------------------------------ CARTE 3D de Côte d'Ivoire
export const MAP_CAM = (t: number, ev: any) => {
  const k = eInOut(prog(t, ev.mapRise, ev.mapRise + 3.7));
  const az = lerp(-0.4, 0.2, k), dist = lerp(28, 23.5, k), el = lerp(0.98, 0.84, k);
  return {pos: [Math.sin(az) * Math.cos(el) * dist, Math.sin(el) * dist, Math.cos(az) * Math.cos(el) * dist] as [number, number, number], look: [0.1, 0, -1.3] as [number, number, number]};
};
export const PILLAR_H = 1.5;
export const Map3D: React.FC<{t: number; ev: any; order: string[]}> = ({t, ev, order}) => {
  const glow = useGlowTex();
  const geo = useMemo(() => {
    const s = new THREE.Shape(CIV.pts.map(([x, y]: number[]) => new THREE.Vector2(x, y)));
    const g = new THREE.ExtrudeGeometry(s, {depth: 0.35, bevelEnabled: true, bevelThickness: 0.06, bevelSize: 0.04, bevelSegments: 4, curveSegments: 8});
    g.rotateX(-Math.PI / 2); return g;
  }, []);
  const edges = useMemo(() => new THREE.EdgesGeometry(geo, 30), [geo]);
  const rise = eOut5(prog(t, ev.mapRise, ev.mapRise + 0.9));
  const {pos, look} = MAP_CAM(t, ev);
  return <ThreeCanvas width={W} height={H} style={{position: 'absolute', inset: 0}} gl={{antialias: true, alpha: true, toneMapping: THREE.ACESFilmicToneMapping}}>
    <Cam pos={pos} look={look} fov={32} />
    <Env intensity={0.7} />
    <ambientLight intensity={0.25} />
    <directionalLight position={[4, 10, 6]} intensity={2.2} />
    <directionalLight position={[-6, 4, -4]} intensity={1.2} color="#ff9a40" />
    <gridHelper args={[40, 40, '#5a3a18', '#2a1d10']} position={[0, -0.02, 0]} />
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]}><planeGeometry args={[18, 18]} /><meshBasicMaterial map={glow} color="#ff7a10" transparent opacity={0.35 * rise} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
    <group position={[0, (rise - 1) * 3, 0]} rotation={[0, (1 - rise) * 1.2, 0]} scale={[1, Math.max(0.01, rise), 1]}>
      <mesh geometry={geo}><meshPhysicalMaterial color="#e07f17" metalness={0.3} roughness={0.45} clearcoat={0.5} emissive="#ff6a00" emissiveIntensity={0.05} /></mesh>
      <lineSegments geometry={edges}><lineBasicMaterial color="#ffd29a" transparent opacity={0.8} /></lineSegments>
      {order.map((c, i) => {
        const [x, y] = (CIV.cities as any)[c]; const t0 = ev.pillars[i]; if (t < t0) return null;
        const k = eBack(prog(t, t0, t0 + 0.4)); const h = PILLAR_H * k; const rip = prog(t, t0, t0 + 1);
        return <group key={c} position={[x, 0.42, -y]}>
          <mesh position={[0, h / 2, 0]}><cylinderGeometry args={[0.07, 0.07, Math.max(h, 0.001), 20]} /><meshStandardMaterial color="#ffffff" emissive="#ffc46b" emissiveIntensity={2.2} /></mesh>
          <mesh position={[0, h, 0]}><sphereGeometry args={[0.16, 24, 16]} /><meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={3} /></mesh>
          <mesh position={[0, h, 0]}><planeGeometry args={[1.6, 1.6]} /><meshBasicMaterial map={glow} color="#ffcf80" transparent opacity={0.9} blending={THREE.AdditiveBlending} depthWrite={false} side={THREE.DoubleSide} /></mesh>
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}><ringGeometry args={[0.15 + rip * 0.9, 0.22 + rip * 0.9, 40]} /><meshBasicMaterial color="#ffd29a" transparent opacity={1 - rip} /></mesh>
        </group>;
      })}
    </group>
    <Particles t={t} n={300} spread={16} seed={5} speed={0.25} size={0.04} opacity={0.6} />
  </ThreeCanvas>;
};

// ------------------------------------------------------------------ CARROUSEL 3D de photos
const roundedRectGeo = (w: number, h: number, r: number) => {
  const s = new THREE.Shape(); const x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  const g = new THREE.ShapeGeometry(s, 12); const uv = g.attributes.uv as THREE.BufferAttribute; const p = g.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, (p.getX(i) - x) / w, (p.getY(i) - y) / h);
  return g;
};
export const Carousel3D: React.FC<{t: number; ev: any; photos: string[]}> = ({t, ev, photos}) => {
  const tex = useTextures(photos.map((p) => staticFile(`img/${p}.jpg`)));
  const geo = useMemo(() => roundedRectGeo(2.7, 3.6, 0.22), []);
  const frame = useMemo(() => roundedRectGeo(2.86, 3.76, 0.28), []);
  const glow = useGlowTex();
  const n = photos.length, R = 5.0;
  const inK = eOut5(prog(t, ev.carIn, ev.carIn + 0.9));
  // rotation rapide puis arrêt sur une photo au moment du tampon
  const spinEnd = ev.carStamp - 0.15;
  const rot = -Math.PI * 2 * (1.25 * eOut(prog(t, ev.carIn, spinEnd))) + (1 - inK) * 1.5;
  const pos: [number, number, number] = [0, 3.4 - 1.0 * inK, 25 - 4 * inK];
  if (!tex) return null;
  return <ThreeCanvas width={W} height={H} style={{position: 'absolute', inset: 0}} gl={{antialias: true, alpha: true, toneMapping: THREE.ACESFilmicToneMapping}}>
    <Cam pos={pos} look={[0, 0.3, 0]} fov={34} />
    <ambientLight intensity={1.1} />
    <group rotation={[0.06, rot, 0]} position={[0, 0, -R + 1.2]}>
      {photos.map((p, i) => {
        const a = (i / n) * Math.PI * 2;
        return <group key={p} position={[Math.sin(a) * R, 0.4, Math.cos(a) * R]} rotation={[0, a, 0]}>
          <mesh geometry={frame} position={[0, 0, -0.01]}><meshBasicMaterial color="#ffffff" /></mesh>
          <mesh geometry={geo}><meshBasicMaterial map={tex[i]} toneMapped={false} /></mesh>
          {/* reflet */}
          <mesh geometry={geo} position={[0, -3.85, 0]} scale={[1, -1, 1]}><meshBasicMaterial map={tex[i]} transparent opacity={0.16} toneMapped={false} /></mesh>
        </group>;
      })}
    </group>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.6, 0]}><planeGeometry args={[30, 30]} /><meshBasicMaterial map={glow} color="#ff7a10" transparent opacity={0.4} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
    <Particles t={t} n={260} spread={16} seed={11} speed={0.3} size={0.05} opacity={0.55} />
  </ThreeCanvas>;
};
