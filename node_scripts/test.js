const URL = "http://localhost:5000/relay/toggle";

const delay = ms => new Promise(r => setTimeout(r, ms));

(async () => {
    for (let i = 1; i <= 10; i++) {
        await fetch(URL, { method: "POST" });
        console.log(`Toggle ${i}`);
        await delay(1000); // 0.5s between toggles
    }
    console.log("Done");
})();
