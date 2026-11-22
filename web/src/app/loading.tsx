export default function Loading() {
  return (
    <div className="grid min-h-[70svh] place-items-center" role="status" aria-label="Chargement">
      <div className="flex flex-col items-center gap-5">
        <span dir="ltr" className="font-display text-5xl tracking-[0.04em] text-paper/15">
          ONELINE<span className="text-accent">.</span>
        </span>
        <span className="relative h-px w-40 overflow-hidden bg-paper/10">
          <span className="absolute inset-y-0 start-0 w-1/3 animate-[loadbar_1.1s_ease-in-out_infinite] bg-accent motion-reduce:animate-none" />
        </span>
      </div>
      <style>{`@keyframes loadbar{0%{transform:translateX(-100%)}100%{transform:translateX(300%)}}`}</style>
    </div>
  );
}
