"use client";
import { motion, AnimatePresence } from "framer-motion";
import Dashboard from "./components/Dashboard";
import Progress from "./components/Progress";
import TextAnim from "./components/TextAnim";
import { useState, useEffect, useRef } from "react";
import Link from "next/link";

export default function Home() {
  
  const [isInView, setIsInView] = useState(false);
  const sectionRef = useRef(null);

  const inViewAnimation = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { duration: 1.5, ease: "easeOut" } },
  };

  // Set up the IntersectionObserver to detect when the section is in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsInView(entry.isIntersecting);  // Update state when the section enters/exits the viewport
      },
      { threshold: 0.5 } // Trigger when 50% of the section is visible
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current); // Start observing the section
    }

    // Cleanup the observer when component unmounts
    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current); // Stop observing
      }
    };
  }, []);
  return (
<<<<<<< HEAD
    <div className="flex flex-col items-center w-full mt-8">
      <motion.div
        initial="hidden"
        whileInView="visible"
        variants={inViewAnimation}
        viewport={{ once: true }}
        className="text-white mt-20 max-w-4xl mx-auto text-center"
      >
        <h1 className="text-6xl md:text-5xl font-bold mb-6">
          <TextAnim/>
        </h1>
        <p className="text-lg md:text-xl mb-8">
          X empowers lease operators with real-time detection and
          predictive insights for hydrate formation, ensuring optimal production
          and minimizing downtime.
        </p>
      </motion.div>
      <div
        className="flex flex-row justify-center items-center gap-10"
      >
        <button className="hover:scale-120 transition-all duration-200 bg-white  px-4 pb-2 pt-3 rounded-xl shadow-lg">
          <Link href={"/login"}>
            <h2 className="text-2xl font-semibold mb-4">Login as Agent</h2>
          </Link>
        </button>
        <button className="hover:scale-120 transition-all duration-200 bg-white  px-4 pb-2 pt-3 rounded-xl shadow-lg">
          <Link href={"/login_admin"}>
          <h2 className="text-2xl font-semibold mb-4">Login as Admin</h2>
          </Link>
        </button>
      </div>
      <div className="flex flex-col items-center justify-center mt-16 text-white w-full">
        <h1 className="text-6xl md:text-5xl font-bold mb-6">  Upload File for ML Analysis</h1>
        <div className="w-[500px] flex flex-col justify-center items-center bg-rose-500 bg-opacity-15 p-4 rounded-lg shadow-lg mb-4 transform hover:scale-105 transition-transform duration-200 ease-in-out">
          <span className="text-white mr-2 font-bold mb-2 text-[30px]">Add .csv file</span>
          <input
            type="file"
            accept=".csv"
            id="csv-upload"
            className="hidden"
            onChange={(event) => {
              const file = event.target.files[0];
              if (file) {
                console.log("File uploaded:", file.name);
              }
            }}
          />
          <label
            htmlFor="csv-upload"
            className="cursor-pointer border-[2px] border-white bg-transparent rounded-md flex flex-row py-2 pl-3 pr-2 hover:bg-black hover:border-none duration-200 hover:text-white font-bold transition-colors"
          >
            <span className="text-white mr-2">Upload</span>
          </label>
        </div>
      </div>
      
      
    </div>
  );
}
