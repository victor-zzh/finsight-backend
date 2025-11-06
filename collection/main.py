import argparse
from pipeline_logic import run_data_collection

def main():
    parser = argparse.ArgumentParser(description="Financial Data Collection Pipeline")
    parser.add_argument("--mode", choices=["full", "incremental", "test"], default="full",
                       help="Collection mode: full (complete refresh), incremental (update recent), test (small sample)")
    parser.add_argument("--companies", nargs="*", help="Specific company codes to process")
    parser.add_argument("--start-date", help="Start date for data collection (YYYYMMDD)")
    parser.add_argument("--end-date", help="End date for data collection (YYYYMMDD)")

    args = parser.parse_args()

    print(f"Starting data collection in {args.mode} mode")
    run_data_collection(args.mode, args.companies, args.start_date, args.end_date)
    print("Data collection completed")

if __name__ == "__main__":
    main()
