import { Hero } from "@/components/home/Hero";
import { Vibes } from "@/components/home/Vibes";
import { ClosingCta, Featured, HowItWorks, RoomCompare, Social, WhyUs } from "@/components/home/Sections";

export default function Home() {
  return (
    <>
      <Hero />
      <Vibes />
      <Featured />
      <RoomCompare />
      <WhyUs />
      <HowItWorks />
      <Social />
      <ClosingCta />
    </>
  );
}
