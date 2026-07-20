export type QuizOptionKey = "A" | "B" | "C" | "D" | "E";

export type QuizOption = {
  key: QuizOptionKey;
  label: string;
};

export type QuizQuestion = {
  id: number;
  prompt: string;
  options: QuizOption[];
};

export const QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: 1,
    prompt: "What's your usual morning mood?",
    options: [
      { key: "A", label: "Peaceful and quiet, I take it slow" },
      { key: "B", label: "Running late but still need coffee" },
      { key: "C", label: "Craving something sweet before work" },
      { key: "D", label: "Enjoying a routine with family" },
      { key: "E", label: "Feeling ready to conquer the day" },
    ],
  },
  {
    id: 2,
    prompt: "Your barista offers a free syrup. Which do you pick?",
    options: [
      { key: "A", label: "None—I like coffee as it is" },
      { key: "B", label: "Vanilla" },
      { key: "C", label: "Caramel" },
      { key: "D", label: "Hazelnut" },
      { key: "E", label: "Surprise me with something seasonal" },
    ],
  },
  {
    id: 3,
    prompt: "A café just released a strange new drink. You...",
    options: [
      { key: "A", label: "Stick with your regular order" },
      { key: "B", label: "Read reviews first" },
      { key: "C", label: "Split one with a friend" },
      { key: "D", label: "Try it immediately" },
      { key: "E", label: "Order it just because it looks interesting" },
    ],
  },
  {
    id: 4,
    prompt: "Which coffee mistake bothers you most?",
    options: [
      { key: "A", label: "Bad presentation" },
      { key: "B", label: "Coffee that isn't strong enough" },
      { key: "C", label: "A drink that's far too sweet" },
      { key: "D", label: "It arrives lukewarm" },
      { key: "E", label: "It looks amazing but tastes disappointing" },
    ],
  },
  {
    id: 5,
    prompt: "What's your ideal café atmosphere?",
    options: [
      { key: "A", label: "Quiet and cozy" },
      { key: "B", label: "Busy and energetic" },
      { key: "C", label: "Friendly and social" },
      { key: "D", label: "Elegant and sophisticated" },
      { key: "E", label: "Modern and aesthetically designed" },
    ],
  },
  {
    id: 6,
    prompt: "Pick a book you'd read all weekend.",
    options: [
      { key: "A", label: "Cozy romance" },
      { key: "B", label: "Mystery thriller" },
      { key: "C", label: "Fantasy adventure" },
      { key: "D", label: "Self-improvement" },
      { key: "E", label: "Historical fiction" },
    ],
  },
  {
    id: 7,
    prompt: "Your bookshelf is mostly...",
    options: [
      { key: "A", label: "Carefully organized" },
      { key: "B", label: "Full of unfinished books" },
      { key: "C", label: "Whatever friends recommended" },
      { key: "D", label: "Old favorites I reread" },
      { key: "E", label: "A mix of everything" },
    ],
  },
  {
    id: 8,
    prompt: "You're choosing a movie tonight.",
    options: [
      { key: "A", label: "Comfort movie" },
      { key: "B", label: "Psychological thriller" },
      { key: "C", label: "Comedy" },
      { key: "D", label: "Documentary" },
      { key: "E", label: "Something visually beautiful" },
    ],
  },
  {
    id: 9,
    prompt: "Which fictional place would you visit?",
    options: [
      { key: "A", label: "Hogwarts (Harry Potter)" },
      { key: "B", label: "Wonderland (Alice in Wonderland)" },
      { key: "C", label: "Pandora (Avatar)" },
      { key: "D", label: "Magic Dimension (Winx Club)" },
      { key: "E", label: "The Shire (The Lord of the Rings)" },
    ],
  },
  {
    id: 10,
    prompt: "Do you usually finish books?",
    options: [
      { key: "A", label: "Always" },
      { key: "B", label: "Usually" },
      { key: "C", label: "Only if they hook me" },
      { key: "D", label: "Rarely" },
      { key: "E", label: "I constantly start new ones" },
    ],
  },
  {
    id: 11,
    prompt: "Which weather instantly improves your mood?",
    options: [
      { key: "A", label: "Gentle rain" },
      { key: "B", label: "Bright sunshine" },
      { key: "C", label: "Crisp autumn air" },
      { key: "D", label: "Snowfall" },
      { key: "E", label: "Thunderstorms" },
    ],
  },
  {
    id: 12,
    prompt: "Your perfect season is...",
    options: [
      { key: "A", label: "Spring" },
      { key: "B", label: "Summer" },
      { key: "C", label: "Autumn" },
      { key: "D", label: "Winter" },
      { key: "E", label: "Every season has something to love" },
    ],
  },
  {
    id: 13,
    prompt: "It's raining outside. What are you doing?",
    options: [
      { key: "A", label: "Reading by the window" },
      { key: "B", label: "Working in a café" },
      { key: "C", label: "Watching movies under a blanket" },
      { key: "D", label: "Taking a nap" },
      { key: "E", label: "Taking photos of the rain" },
    ],
  },
  {
    id: 14,
    prompt: "Sunrise or sunset?",
    options: [
      { key: "A", label: "Sunrise" },
      { key: "B", label: "Sunset" },
      { key: "C", label: "Both" },
      { key: "D", label: "Depends on my mood" },
      { key: "E", label: "Neither—I prefer cloudy days" },
    ],
  },
  {
    id: 15,
    prompt: "Choose a vacation.",
    options: [
      { key: "A", label: "Mountain cabin" },
      { key: "B", label: "Big city" },
      { key: "C", label: "Beach resort" },
      { key: "D", label: "European village" },
      { key: "E", label: "Anywhere I've never been" },
    ],
  },
  {
    id: 16,
    prompt: "Your friends describe you as...",
    options: [
      { key: "A", label: "Calm" },
      { key: "B", label: "Reliable" },
      { key: "C", label: "Funny" },
      { key: "D", label: "Creative" },
      { key: "E", label: "Adventurous" },
    ],
  },
  {
    id: 17,
    prompt: "When making decisions...",
    options: [
      { key: "A", label: "I trust logic" },
      { key: "B", label: "I trust my intuition" },
      { key: "C", label: "I ask others" },
      { key: "D", label: "I overthink everything" },
      { key: "E", label: "I decide quickly" },
    ],
  },
  {
    id: 18,
    prompt: "Your phone battery is at 5%.",
    options: [
      { key: "A", label: "I already have a charger" },
      { key: "B", label: "Mild panic" },
      { key: "C", label: "It'll be fine" },
      { key: "D", label: "Borrow someone's charger" },
      { key: "E", label: "Time to disconnect" },
    ],
  },
  {
    id: 19,
    prompt: "Your desk usually looks...",
    options: [
      { key: "A", label: "Perfectly organized" },
      { key: "B", label: "Organized chaos" },
      { key: "C", label: "Covered in snacks" },
      { key: "D", label: "Minimalist" },
      { key: "E", label: "Depends on the week" },
    ],
  },
  {
    id: 20,
    prompt: "You're an hour early. What do you do?",
    options: [
      { key: "A", label: "Read a book" },
      { key: "B", label: "Explore nearby" },
      { key: "C", label: "Get a drink" },
      { key: "D", label: "People-watch" },
      { key: "E", label: "Catch up on messages" },
    ],
  },
  {
    id: 21,
    prompt: "Which sounds most satisfying?",
    options: [
      { key: "A", label: "Crossing off a to-do list" },
      { key: "B", label: "Learning something new" },
      { key: "C", label: "Making someone laugh" },
      { key: "D", label: "Creating something beautiful" },
      { key: "E", label: "Trying something unfamiliar" },
    ],
  },
  {
    id: 22,
    prompt: "Pick a weekend activity.",
    options: [
      { key: "A", label: "Visiting a bookstore" },
      { key: "B", label: "Hiking" },
      { key: "C", label: "Brunch with friends" },
      { key: "D", label: "Baking at home" },
      { key: "E", label: "Exploring a new café" },
    ],
  },
  {
    id: 23,
    prompt: "If you won a free afternoon...",
    options: [
      { key: "A", label: "Nap" },
      { key: "B", label: "Work on a hobby" },
      { key: "C", label: "Meet friends" },
      { key: "D", label: "Visit somewhere peaceful" },
      { key: "E", label: "Wander with no plan" },
    ],
  },
  {
    id: 24,
    prompt: "Which room feels most like home?",
    options: [
      { key: "A", label: "Library" },
      { key: "B", label: "Kitchen" },
      { key: "C", label: "Living room with friends" },
      { key: "D", label: "Bedroom watching a movie" },
      { key: "E", label: "Balcony overlooking a city" },
    ],
  },
  {
    id: 25,
    prompt: "Choose a soundtrack.",
    options: [
      { key: "A", label: "Lo-fi beats" },
      { key: "B", label: "Classical piano" },
      { key: "C", label: "Indie folk" },
      { key: "D", label: "Jazz" },
      { key: "E", label: "Pop hits" },
    ],
  },
  {
    id: 26,
    prompt: "Which color palette speaks to you?",
    options: [
      { key: "A", label: "Earth tones" },
      { key: "B", label: "Black and white" },
      { key: "C", label: "Pastels" },
      { key: "D", label: "Rich jewel tones" },
      { key: "E", label: "Bright colors" },
    ],
  },
  {
    id: 27,
    prompt: "Pick a dessert.",
    options: [
      { key: "A", label: "Tiramisu" },
      { key: "B", label: "Dark chocolate cake" },
      { key: "C", label: "Cheesecake" },
      { key: "D", label: "Cinnamon roll" },
      { key: "E", label: "Lemon tart" },
    ],
  },
  {
    id: 28,
    prompt: "Which scent do you enjoy most?",
    options: [
      { key: "A", label: "Fresh rain" },
      { key: "B", label: "Vanilla" },
      { key: "C", label: "Cinnamon" },
      { key: "D", label: "Lavender" },
      { key: "E", label: "Freshly baked pastries" },
    ],
  },
  {
    id: 29,
    prompt: "What's your ideal workspace?",
    options: [
      { key: "A", label: "Quiet library" },
      { key: "B", label: "Trendy café" },
      { key: "C", label: "Home office" },
      { key: "D", label: "Outdoor patio" },
      { key: "E", label: "Creative studio" },
    ],
  },
  {
    id: 30,
    prompt: "Which quote resonates with you most?",
    options: [
      { key: "A", label: '"Enjoy the little things."' },
      { key: "B", label: '"Stay curious."' },
      { key: "C", label: '"Collect moments, not things."' },
      { key: "D", label: '"Home is where you\'re happiest."' },
      { key: "E", label: '"Life begins outside your comfort zone."' },
    ],
  },
];

export const QUIZ_SESSION_LENGTH = 15;
export const COFFEE_PREFERENCE_COUNT = 2;

/** Always include these taste/preference questions so matches stay coffee-grounded. */
export const COFFEE_PREFERENCE_QUESTIONS: QuizQuestion[] = [
  {
    id: 101,
    prompt: "What job do you want your coffee to do today?",
    options: [
      { key: "A", label: "Wake me up and keep me focused." },
      { key: "B", label: "Be something comforting while I relax." },
      { key: "C", label: "Satisfy my sweet tooth." },
      { key: "D", label: "Refresh me and cool me down." },
      { key: "E", label: "Surprise me with something fun and different." },
    ],
  },
  {
    id: 102,
    prompt: "If a barista offered one free add-on, which would you choose?",
    options: [
      { key: "A", label: "Nothing—I like coffee as it is" },
      { key: "B", label: "A flavored syrup (vanilla, caramel, etc.)" },
      { key: "C", label: "Extra espresso for a stronger kick" },
      { key: "D", label: "Whipped cream or cold foam" },
      { key: "E", label: "Surprise me with something unique" },
    ],
  },
  {
    id: 103,
    prompt: "Which coffee experience sounds the most enjoyable?",
    options: [
      { key: "A", label: "Reading in a quiet café with a warm drink" },
      { key: "B", label: "Grabbing an iced coffee while exploring the city" },
      { key: "C", label: "Catching up with friends over specialty drinks" },
      { key: "D", label: "Sitting outside with a simple black coffee" },
      { key: "E", label: "Visiting a café known for creative seasonal menus" },
    ],
  },
  {
    id: 104,
    prompt: "How often do you treat yourself to something sweet?",
    options: [
      {
        key: "A",
        label: "Rarely — I usually prefer savory or less sweet flavors.",
      },
      { key: "B", label: "Occasionally — a dessert is a special treat." },
      {
        key: "C",
        label: "A little something sweet with coffee is always welcome.",
      },
      {
        key: "D",
        label: "I have a strong sweet tooth — dessert is part of my routine.",
      },
      {
        key: "E",
        label: "I love trying new desserts, pastries, and sweet creations.",
      },
    ],
  },
];

function shuffleQuestions(questions: QuizQuestion[]): QuizQuestion[] {
  const pool = [...questions];

  for (let i = pool.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }

  return pool;
}

/**
 * Builds a quiz session with exactly `coffeeCount` coffee-preference questions
 * and fills the rest from the general personality pool.
 */
export function pickQuizSession(
  generalQuestions: QuizQuestion[] = QUIZ_QUESTIONS,
  coffeeQuestions: QuizQuestion[] = COFFEE_PREFERENCE_QUESTIONS,
  totalCount: number = QUIZ_SESSION_LENGTH,
  coffeeCount: number = COFFEE_PREFERENCE_COUNT,
): QuizQuestion[] {
  const selectedCoffee = shuffleQuestions(coffeeQuestions).slice(
    0,
    Math.min(coffeeCount, coffeeQuestions.length),
  );
  const remainingSlots = Math.max(totalCount - selectedCoffee.length, 0);
  const selectedGeneral = shuffleQuestions(generalQuestions).slice(
    0,
    remainingSlots,
  );

  return shuffleQuestions([...selectedCoffee, ...selectedGeneral]);
}

/** @deprecated Prefer pickQuizSession for quiz runs. */
export function pickRandomQuestions(
  questions: QuizQuestion[],
  count: number,
): QuizQuestion[] {
  return shuffleQuestions(questions).slice(0, Math.min(count, questions.length));
}
