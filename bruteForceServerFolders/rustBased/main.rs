use std::env;
use std::process;
use std::time::SystemTime;
use chrono;

fn get_current_time() -> String{
    // returns the local time + date in a string
    return chrono::offset::Local::now().to_string().replace(" ","_");
}

fn usage() {
    println!("");
    println!("Usage: PROG [-FLAGS] URL\n");
    println!("Description:\nADD DESCRIPTION\n");
    println!("Flags:");
    println!("    -h        Print this help and exit");
    println!("    -d        Uses the specified directory to store the results of the brute force attempt");
    println!("              The default name is \"Brute Force Results\".");
    println!("    -f        Uses the specified file to store the results of the brute force attempt");
    println!("              The default name is Url_theCurrenTime.txt.");
    println!("    -m        Uses the specified integer as the maximum length of the bute force attempt. The maxLength is 4 by default.");
    println!("    -c        The default list are the upper and lowercase ascii letters");
    println!("              If you want to specify your own character List you can combine the following:");
    println!("              l for lowercase, u for uppercase, d for digits, p for punktuation or a for all of them.");
    println!("    -n        The script will use ANSI color codes to dye the output in case an Url is found");
    println!("              This is false by default. Use the -n flag to disable it. This only works with an registry Tweak on Windows.\n");
    println!("Required commands");
    println!("    URL       Uses the specified Url as the base for the brute force attempt");
    println!("              This must be a complete link like https://www.google.com/. The https:// must be included.");
    println!("");
    process::exit(0x0100);
}

fn main() {
    let flag_list = ["-h","-d","-f","-m","-c","-n"];

    let mut directory = "Brute_Force_Results";
    let mut file = "Results";
    let mut max_length: u8 = 4;
    let mut char_list = "";
    let mut url = "";

    let mut args: Vec<String> = env::args().collect();
    // removes the scriptname from the list of args
    args.remove(0);
    
    if args.len() < 1 {
        println!("You need to supply a URL! Do \"PROG -h\" for more info!");
        process::exit(0x0100);
    }

    for arg in args {
        if arg == "-h" {
            usage();
        } else if arg == "-d" {
            println!("The -d flag was set!");
        } else if arg == "-f" {
            println!("The -f flag was set!");
        } else if arg == "-m" {
            println!("The -m flag was set!");
        } else if arg == "-c" {
            println!("The -c flag was set!");
        } else if arg == "-n" {
            println!("The -n flag was set!");
        } else {
            println!("\"{}\" is not a valid flag! Do \"PROG -h\" for help!", arg);
            process::exit(0x0100);
        }
    }
    println!("Time: {}",get_current_time());
}
