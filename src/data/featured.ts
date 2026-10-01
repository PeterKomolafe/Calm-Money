// Press logos: the same six, in the same order, as the TV credits on peterkomolafe.com. [file, name, width, height]
export const featured = [
  ['bbc', 'BBC', 145, 45], ['channel-4', 'Channel 4', 38, 51], ['itv', 'ITV', 79, 42],
  ['sky-news', 'Sky News', 138, 38], ['channel-5', 'Channel 5', 40, 56], ['lorraine', 'Lorraine', 144, 37],
] as const;

// Size each logo by area so wide wordmarks and square marks look equally heavy
export const logoHeight = (file: string, w: number, h: number) =>
  Math.round(Math.max(14, Math.min(30, Math.sqrt(1100 / (w / h)))));
