"use client";
import Navbar from "@/app/components/navbar";
import { Line } from "react-chartjs-2";
import Footer from "@/app/components/footer";
import {
    Chart,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
} from "chart.js";
import { useEffect, useState } from "react";
import "dotenv/config";

console.log(process.env.NEXT_PUBLIC_API_URL);

export default function Home() {
    // -------------------------------------
    const [dataset, setDataset] = useState([]);
    const [fast, setFast] = useState(1);
    const [slow, setSlow] = useState(3);
    const [now, setNow] = useState(5);
    Chart.register(CategoryScale, LinearScale, PointElement, LineElement);
    const data = {
        labels: ["", "", "", "", "", ""],
        datasets: [
            {
                label: "button Data",
                data: dataset,
                fill: false,
                borderColor: "rgb(75, 192, 192)",
                tension: 0.1,
            },
        ],
    };
    const options_line = {
        scales: {
            x: {
                type: "category",
                // Additional configuration for the x-axis can go here
            },
            y: {
                type: "linear",
                // Additional configuration for the y-axis can go here
            },
        },
    };
    useEffect(() => {
        const lowValue = Math.min(...dataset);
        const highValue = Math.max(...dataset);
        const lastValue = dataset[dataset.length - 1];
        setNow(lastValue);
        setFast(lowValue);
        setSlow(highValue);
    }, [dataset]);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_API_URL)
            .then((response) => response.text())
            .then((data) => {
                const parsedData = JSON.parse(data);
                const convertedData = parsedData.map((value) => value / 1000);
                setDataset(convertedData);
            })
            .catch((error) => console.error("Error fetching data:", error));
    }, []);
    // -----------------------------------

    return (
        <>
            <Navbar />
            {/* ------------------ */}
            <section className="flex flex-row justify-evenly pt-10 pb-10 flex-wrap">
                <div
                    href="#"
                    className="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 w-64 mb-2 mb:mb-0"
                >
                    <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                        🚀 เร็วที่สุด
                    </h5>
                    <p className="font-normal text-gray-700">{fast} วินาที</p>
                </div>
                <div
                    href="#"
                    className="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 w-64 mb-2 mb:mb-0"
                >
                    <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                        🔗 ล่าสุด
                    </h5>
                    <p className="font-normal text-gray-700">{now} วินาที</p>
                </div>
                <div
                    href="#"
                    className="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 w-64 mb-2 mb:mb-0"
                >
                    <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                        💤 ช้าที่สุด
                    </h5>
                    <p className="font-xl text-gray-700 ">{slow} วินาที</p>
                </div>
            </section>

            {/* ------------------------ */}
            <section className="flex justify-center">
                <div className=" w-1/2">
                    <Line options={options_line} data={data} />
                </div>
            </section>
            <div className="fixed bottom-0 w-full">
                <Footer />
            </div>
        </>
    );
}
