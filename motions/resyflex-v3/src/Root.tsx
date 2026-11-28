import React from 'react';
import {Composition} from 'remotion';
import {ResyFlex3} from './ResyFlex3';
import TL from './timeline.json';
export const RemotionRoot: React.FC = () => (
  <Composition id="ResyFlex3" component={ResyFlex3} durationInFrames={Math.round(TL.duration * TL.fps)} fps={TL.fps} width={TL.width} height={TL.height} />
);
