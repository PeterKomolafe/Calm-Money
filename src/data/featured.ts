// Press logos, cropped from Peter's own 'As featured on' strip: [file, name, width, height]
export const featured = [
  ['channel-4', 'Channel 4', 38, 51], ['sky-news', 'Sky News', 138, 38], ['itv', 'ITV', 79, 42],
  ['lorraine', 'Lorraine', 144, 37], ['stephs-packed-lunch', 'Steph’s Packed Lunch', 57, 56], ['bbc', 'BBC', 145, 45],
  ['channel-5', 'Channel 5', 40, 56], ['the-times', 'The Times', 88, 37], ['metro', 'Metro', 121, 39],
] as const;

// Size each logo by area so wide wordmarks and square marks look equally heavy; Steph's gets 10% more
export const logoHeight = (file: string, w: number, h: number) =>
  Math.round(Math.max(14, Math.min(30, Math.sqrt(1100 / (w / h)))) * (file === 'stephs-packed-lunch' ? 1.1 : 1));
