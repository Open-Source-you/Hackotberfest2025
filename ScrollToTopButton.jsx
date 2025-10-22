import { useEffect, useState } from "react";
import { ArrowUpCircle } from "lucide-react";

const ScrollToTopButton = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      setIsVisible(window.scrollY > 300);
    };
    window.addEventListener("scroll", toggleVisibility);
    return () => window.removeEventListener("scroll", toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div
      className={`fixed bottom-6 right-6 z-50 transition-all duration-500 ${
        isVisible
          ? "opacity-100 translate-y-0"
          : "opacity-0 translate-y-10 pointer-events-none"
      }`}
    >
      <button
        onClick={scrollToTop}
        className="group bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-indigo-600 hover:to-blue-500 text-white p-3 rounded-full shadow-lg transition-all duration-300 ease-out hover:shadow-2xl focus:outline-none"
        aria-label="Scroll to top"
      >
        <ArrowUpCircle
          className="h-7 w-7 transition-transform duration-300 group-hover:-translate-y-1 group-hover:rotate-12"
        />
      </button>

      <span className="absolute bottom-12 right-1/2 translate-x-1/2 opacity-0 group-hover:opacity-100 bg-gray-900 text-white text-xs rounded-md py-1 px-2 shadow-md transition-all duration-300">
        Back to top
      </span>
    </div>
  );
};

export default ScrollToTopButton;
