import React from 'react';
import {Composition} from 'remotion';
import {ResyFlex} from './ResyFlex';
import TL from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition id="ResyFlex" component={ResyFlex} durationInFrames={Math.round(TL.duration * TL.fps)} fps={TL.fps} width={TL.width} height={TL.height} />
);
