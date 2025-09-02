"""
Financial Dashboard Application
Main entry point for the integrated financial analysis system.

This application validates data, runs extraction pipeline if needed,
and launches either CLI or web interface for financial data analysis.

Author: Felipe Ferreira de Carvalho
"""

import os
import sys
import pandas as pd
import argparse
from datetime import datetime
from typing import Optional

def print_banner():
    """Display application banner"""
    print("=" * 70)
    print("🏦 FINANCIAL DASHBOARD - INTEGRATED ANALYSIS SYSTEM")
    print("   REXP & DIPD Financial Data Analysis with AI Assistant")
    print("   by Felipe Ferreira de Carvalho")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def get_project_paths():
    """Get all necessary project paths"""
    current_dir = os.getcwd()
    
    paths = {
        'root': current_dir,
        'data_dir': os.path.join(current_dir, 'data'),
        'processed_dir': os.path.join(current_dir, 'data', 'processed'),
        'raw_dir': os.path.join(current_dir, 'data', 'raw'),
        'financial_data': os.path.join(current_dir, 'data', 'processed', 'financial_data.csv'),
        'pipeline_script': os.path.join(current_dir, 'src', 'extraction', 'pipeline.py'),
        'chat_dir': os.path.join(current_dir, 'src', 'chat')
    }
    
    return paths

def check_data_exists(file_path: str) -> bool:
    """Check if financial data file exists"""
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

def validate_data_structure(file_path: str) -> tuple[bool, Optional[str]]:
    """
    Validate the structure of financial_data.csv
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_columns = {
        'Simbol', 'file_name', 'Revenue', 'Cost of Goods Sold (COGS)', 
        'Gross Profit', 'Operating Expenses', 'Operating Income', 
        'Net Income', 'Report Date'
    }
    
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if file is empty
        if len(df) == 0:
            return False, "Data file is empty"
        
        # Check for required columns
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check for valid companies
        valid_companies = {'REXP', 'DIPD'}
        actual_companies = set(df['Simbol'].unique())
        if not actual_companies.issubset(valid_companies):
            return False, f"Invalid companies found: {actual_companies - valid_companies}"
        
        # Check for numeric columns
        numeric_columns = ['Revenue', 'Cost of Goods Sold (COGS)', 'Gross Profit', 
                          'Operating Expenses', 'Operating Income', 'Net Income']
        
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                return False, f"Column '{col}' should be numeric"
        
        # Check date column
        try:
            pd.to_datetime(df['Report Date'])
        except:
            return False, "Report Date column has invalid date format"
        
        # Minimum data requirements
        if len(df) < 4:  # At least 2 quarters per company
            return False, "Insufficient data records (minimum 4 records required)"
        
        return True, None
        
    except Exception as e:
        return False, f"Error reading data file: {str(e)}"

def get_user_confirmation(message: str) -> bool:
    """Get Y/N confirmation from user"""
    while True:
        try:
            response = input(f"{message} (Y/N): ").strip().upper()
            if response in ['Y', 'YES']:
                return True
            elif response in ['N', 'NO']:
                return False
            else:
                print("Please enter Y or N")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)

def run_extraction_pipeline(pipeline_path: str) -> bool:
    """
    Run the extraction pipeline
    
    Returns:
        bool: Success status
    """
    if not os.path.exists(pipeline_path):
        print(f"❌ Pipeline script not found: {pipeline_path}")
        return False
    
    print("🔄 Running extraction pipeline...")
    print(f"   Pipeline location: {pipeline_path}")
    print("   This may take a few minutes...")
    print()
    
    try:
        # Change to the pipeline directory
        original_dir = os.getcwd()
        pipeline_dir = os.path.dirname(pipeline_path)
        
        # Add the source directory to Python path
        src_dir = os.path.join(original_dir, 'src', 'extraction')
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        # Import and run the pipeline
        try:
            from src.extraction.pipeline import LLMExtractionPipeline
            
            pipeline = LLMExtractionPipeline()
            pipeline.run()
            
            print("✅ Pipeline completed successfully!")
            return True
            
        except ImportError as e:
            print(f"❌ Failed to import pipeline: {e}")
            return False
        except Exception as e:
            print(f"❌ Pipeline execution failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error running pipeline: {e}")
        return False
    finally:
        # Restore original directory
        os.chdir(original_dir)

def launch_web_app(paths: dict):
    """Launch the web dashboard"""
    try:
        # Add chat directory to path
        if paths['chat_dir'] not in sys.path:
            sys.path.insert(0, paths['chat_dir'])
        
        from src.chat.integrated_dash import IntegratedFinancialDashboard
        
        print("🌐 LAUNCHING WEB DASHBOARD")
        print("=" * 50)
        print("Features:")
        print("  📊 Interactive financial charts")
        print("  🤖 AI-powered query system")
        print("  💬 Natural language financial analysis")
        print("  🎯 Context-aware responses")
        print()
        print("🚀 Starting server...")
        print("   URL: http://localhost:8050")
        print("   Press Ctrl+C to stop")
        print("=" * 50)
        
        dashboard = IntegratedFinancialDashboard(data_path=paths['financial_data'])
        dashboard.run_dashboard(debug=False, port=8050)
        
    except ImportError as e:
        print(f"❌ Failed to import dashboard module: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install dash plotly pandas anthropic python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching web app: {e}")
        sys.exit(1)

def launch_cli_app(paths: dict):
    """Launch the CLI interface"""
    try:
        # Add chat directory to path
        if paths['chat_dir'] not in sys.path:
            sys.path.insert(0, paths['chat_dir'])
        
        from src.chat.integrated_dash import StandaloneQuerySystem
        
        print("💻 LAUNCHING CLI ASSISTANT")
        print("=" * 50)
        print("Features:")
        print("  🤖 AI financial analyst")
        print("  💬 Natural language queries")
        print("  📊 Data-driven insights")
        print("  ⚡ Fast terminal interface")
        print("=" * 50)
        
        cli_system = StandaloneQuerySystem(data_path=paths['financial_data'])
        cli_system.run_cli_session()
        
    except ImportError as e:
        print(f"❌ Failed to import CLI module: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install anthropic pandas python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching CLI app: {e}")
        sys.exit(1)

def main():
    """Main application entry point"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Financial Dashboard - Integrated Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python app.py              # Launch web dashboard (default)
            python app.py --web        # Launch web dashboard
            python app.py --cli        # Launch CLI assistant
            python app.py --force      # Force pipeline re-extraction
        """
    )
    
    parser.add_argument('--web', action='store_true', 
                       help='Launch web dashboard (default)')
    parser.add_argument('--cli', action='store_true', 
                       help='Launch CLI assistant')
    parser.add_argument('--force', action='store_true',
                       help='Force data re-extraction')
    
    args = parser.parse_args()
    
    # Default to web if no mode specified
    if not args.cli:
        args.web = True
    
    # Display banner
    print_banner()
    
    # Get project paths
    paths = get_project_paths()
    
    print("PROJECT STRUCTURE VALIDATION")
    print(f"✅   Root directory: {paths['root']}")
    print(f"✅   Data directory: {paths['data_dir']}")
    print(f"✅   Financial data: {paths['financial_data']}")
    print()
    
    # Create necessary directories
    os.makedirs(paths['processed_dir'], exist_ok=True)
    
    # Step 1: Check if data exists
    print("DATA EXISTENCE CHECK")
    
    data_exists = check_data_exists(paths['financial_data'])
    
    if args.force:
        print("⚠️  Force flag detected - will re-extract data regardless")
        data_exists = False
    elif data_exists:
        print("✅ Financial data file found")
        file_size = os.path.getsize(paths['financial_data'])
        print(f"   File size: {file_size:,} bytes")
    else:
        print("❌ Financial data file not found or empty")
    
    print()
    
    # Step 1.1: Request extraction if needed
    if not data_exists:
        print("DATA EXTRACTION REQUIRED")
        
        if not os.path.exists(paths['pipeline_script']):
            print(f"❌ Pipeline script not found: {paths['pipeline_script']}")
            print("Please ensure the project structure is correct.")
            sys.exit(1)
        
        # Check if raw data exists
        if not os.path.exists(paths['raw_dir']):
            print(f"❌ Raw data directory not found: {paths['raw_dir']}")
            print("Please ensure raw data files are available for extraction.")
            sys.exit(1)
        
        should_extract = get_user_confirmation("Do you want to run the data extraction pipeline?")
        
        if not should_extract:
            print("❌ Data extraction declined. Cannot proceed without data.")
            sys.exit(0)
        
        # Run extraction pipeline
        success = run_extraction_pipeline(paths['pipeline_script'])
        
        if not success:
            print("❌ Data extraction failed. Cannot proceed.")
            sys.exit(1)
        
        print()
    
    # Step 2: Validate data structure
    print("DATA STRUCTURE VALIDATION")
    
    is_valid, error_message = validate_data_structure(paths['financial_data'])
    
    if is_valid:
        print("✅ Data structure is valid")
        
        # Display data summary
        try:
            df = pd.read_csv(paths['financial_data'])
            print(f"   Records: {len(df)}")
            print(f"   Companies: {', '.join(df['Simbol'].unique())}")
            print(f"   Date range: {df['Report Date'].min()} to {df['Report Date'].max()}")
        except:
            pass
            
    else:
        print(f"❌ Data structure validation failed: {error_message}")
        print()
        
        # Step 2.1: Delete invalid file and re-extract
        should_reextract = get_user_confirmation("Delete invalid data and re-extract?")
        
        if not should_reextract:
            print("❌ Cannot proceed with invalid data structure.")
            sys.exit(1)
        
        # Delete invalid file
        if os.path.exists(paths['financial_data']):
            os.remove(paths['financial_data'])
            print(f"🗑️  Deleted invalid data file: {paths['financial_data']}")
        
        # Run extraction pipeline again
        success = run_extraction_pipeline(paths['pipeline_script'])
        
        if not success:
            print("❌ Data re-extraction failed. Cannot proceed.")
            sys.exit(1)
        
        # Re-validate
        is_valid, error_message = validate_data_structure(paths['financial_data'])
        
        if not is_valid:
            print(f"❌ Data structure still invalid after re-extraction: {error_message}")
            sys.exit(1)
        
        print("✅ Data structure is now valid after re-extraction")
    
    print()
    
    # Step 3: Initialize application
    print("APPLICATION INITIALIZATION")
    
    if args.cli:
        print("Launching CLI mode...")
        launch_cli_app(paths)
    elif args.web:
        print("Launching web mode...")
        launch_web_app(paths)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)