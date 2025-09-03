import dash
import anthropic
import os
import pandas as pd
from dash import dcc, html, Input, Output, State
from datetime import datetime
from dotenv import load_dotenv
from .constants import SYS_PROMPT_AGENT, COLOR_MAP
from .plots import create_metric_trend_chart, create_profitability_comparison

load_dotenv()

class IntegratedFinancialDashboard:
    def __init__(
            self, data_path: str = None, max_context_rows: int = 35,
            max_tokens:int = 4096, model_name:str = "claude-sonnet-4-20250514" ):
        """
        Initialize the Integrated Financial Dashboard with LLM capabilities
        """
        if data_path is None:
            data_path = os.path.join(os.getcwd(), 'data', 'processed', 'financial_data.csv')
        
        self.data_path = data_path
        self.max_context_rows = max_context_rows
        self.df = None
        self.app = None
        self.client = anthropic.Anthropic()
        self.color_map = COLOR_MAP
        self.system_prompt = SYS_PROMPT_AGENT
        self.model_name = model_name
        self.max_tokens = max_tokens

    def load_and_process_data(self):
        """Load and process the financial data"""
        try:
            self.df = pd.read_csv(self.data_path)
            
            # Convert Report Date to datetime
            self.df['Report Date'] = pd.to_datetime(self.df['Report Date'])
            
            # Extract quarter and year
            self.df['Quarter'] = self.df['Report Date'].dt.quarter
            self.df['Year'] = self.df['Report Date'].dt.year
            self.df['Quarter_Year'] = self.df['Year'].astype(str) + '-Q' + self.df['Quarter'].astype(str)
            
            # Calculate additional metrics
            self.df['Gross Margin %'] = (self.df['Gross Profit'] / self.df['Revenue']) * 100
            self.df['Operating Margin %'] = (self.df['Operating Income'] / self.df['Revenue']) * 100
            self.df['Net Margin %'] = (self.df['Net Income'] / self.df['Revenue']) * 100
            
            # Sort by date
            self.df = self.df.sort_values('Report Date')
            
            print(f"Data loaded successfully: {len(self.df)} records")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def prepare_context_data(self) -> str:
        """Prepare contextual financial data for the LLM"""
        if self.df is None or len(self.df) == 0:
            return "No financial data available."
        
        total_rows = len(self.df)
        if total_rows <= self.max_context_rows:
            context_df = self.df.copy()
        else:
            recent_data = self.df.tail(self.max_context_rows // 2)
            historical_data = self.df.head(self.max_context_rows // 2)
            context_df = pd.concat([historical_data, recent_data]).drop_duplicates()
        

        context_parts = []
        context_parts.append("=== FINANCIAL DATA SUMMARY ===")
        context_parts.append(f"Total Records: {total_rows}")
        context_parts.append(f"Companies: {', '.join(self.df['Simbol'].unique())}")
        context_parts.append(f"Date Range: {self.df['Report Date'].min().strftime('%Y-%m-%d')} to {self.df['Report Date'].max().strftime('%Y-%m-%d')}")
        context_parts.append("")
        
        key_columns = [
            'Simbol', 'Quarter_Year', 'Revenue', 'Gross Profit', 
            'Operating Income', 'Net Income', 'Gross Margin %', 
            'Operating Margin %', 'Net Margin %'
        ]

        context_df_formatted = context_df[key_columns].copy()
        
        financial_cols = ['Revenue', 'Gross Profit', 'Operating Income', 'Net Income']
        for col in financial_cols:
            if col in context_df_formatted.columns:
                context_df_formatted[col] = context_df_formatted[col].apply(lambda x: f"Rn{x:,.0f}")
        
        margin_cols = ['Gross Margin %', 'Operating Margin %', 'Net Margin %']
        for col in margin_cols:
            if col in context_df_formatted.columns:
                context_df_formatted[col] = context_df_formatted[col].apply(lambda x: f"{x:.1f}%")
        
        context_parts.append("=== DETAILED FINANCIAL DATA ===")
        context_parts.append(context_df_formatted.to_string(index=False))
        
        if total_rows > self.max_context_rows:
            context_parts.append(f"\nNOTE: Showing {len(context_df)} of {total_rows} total records due to context limitations.")
        
        return "\n".join(context_parts)

    def query_financial_data(self, user_query: str) -> str:
        """Process user query and generate LLM response"""
        if self.df is None:
            return "No financial data loaded. Please load data first."
        
        context_data = self.prepare_context_data()
        
        full_prompt = f"""Financial Data Context:
{context_data}

User Query: {user_query}

Please provide a comprehensive answer based on the financial data above. Include specific numbers, dates, and calculations where relevant. Use markdown formatting for better readability."""

        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"



    def setup_dash_app(self):
        """Setup Dash application with LLM integration"""
        self.app = dash.Dash(__name__)
        
        companies = self.df['Simbol'].unique().tolist()
        
        # Sample questions for quick access
        sample_questions = [
            "What is the revenue trend for both companies?",
            "Compare the profitability margins between REXP and DIPD",
            "Which company has better financial performance?",
            "What was the highest revenue quarter for each company?",
            "Analyze the cost structure differences between the companies",
            "What seasonal patterns do you see in the data?"
        ]
        
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("🏦 Integrated Financial Dashboard with AI Assistant", 
                    style={'textAlign': 'center', 'marginBottom': '10px', 'color': '#2c3e50'}),
                html.H4("by Felipe Ferreira de Carvalho", 
                    style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#6c757d'}),
            ]),
            
            # Main content - side by side
            html.Div([
                # Left side - Dashboard
                html.Div([
                    # Controls
                    html.Div([
                        html.Div([
                            html.Label("Select Companies:", style={'fontWeight': 'bold'}),
                            dcc.Checklist(
                                id='company-selector',
                                options=[{'label': comp, 'value': comp} for comp in companies],
                                value=companies,
                                inline=True,
                                style={'margin': '10px 0'}
                            )
                        ], style={'marginBottom': '15px'}),
                        
                        html.Div([
                            html.Label("Select Metric:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='metric-selector',
                                options=[
                                    {'label': 'Revenue', 'value': 'Revenue'},
                                    {'label': 'Gross Profit', 'value': 'Gross Profit'},
                                    {'label': 'Operating Income', 'value': 'Operating Income'},
                                    {'label': 'Net Income', 'value': 'Net Income'}
                                ],
                                value='Revenue'
                            )
                        ])
                    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px', 'marginBottom': '20px'}),
                    
                    # Charts
                    dcc.Graph(id='metric-trend',style={'height':'32%'}),
                    dcc.Graph(id='profitability-analysis',style={'height':'50%'})
                    
                ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '20px'}),
                
                # Right side - Chat
                html.Div([
                    html.H3("🤖 AI Financial Assistant", style={'color': '#495057', 'marginBottom': '20px'}),
                    
                    # Quick questions
                    html.Div([
                        html.Label("Quick Questions:", style={
                            'fontSize': '14px', 'color': '#666'}),
                        html.Div([
                            html.Button(q, id=f'sample-q-{i}',
                                    style={'margin': '5px', 'padding': '8px 12px', 'fontSize': '12px',
                                            'backgroundColor': '#e3f2fd', 'border': '1px solid #2196f3',
                                            'borderRadius': '4px', 'cursor': 'pointer'})
                            for i, q in enumerate(sample_questions[:3])
                        ], style={'marginBottom': '15px','display':'grid'})
                    ]),
                    
                    # Text input
                    dcc.Textarea(
                        id='user-query',
                        placeholder='Ask anything about the financial data...',
                        style={
                            'width': '100%',
                            'height': '80px',
                            'marginBottom': '10px',
                            'borderRadius': '4px'}
                    ),
                    
                    # Submit button
                    html.Button('🔍 Analyze', id='submit-query', 
                            style={'padding': '10px 20px', 'backgroundColor': '#007bff', 'color': 'white', 
                                    'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer', 
                                    'fontWeight': 'bold', 'marginBottom': '20px'}),
                    
                    # Response area
                    html.Div([
                        html.H4("Welcome to the AI Financial Assistant! 🤖", style={'color': '#28a745'}),
                        html.P("Ask any question about REXP and DIPD financial performance."),
                        html.Ul([
                            html.Li("📈 Revenue and profitability analysis"),
                            html.Li("📊 Comparative performance"),
                            html.Li("🔍 Trend identification"),
                            html.Li("💹 Financial calculations")
                        ]),
                        html.P("Click a quick question or type your own!", style={'fontStyle': 'italic', 'color': '#666'})
                    ], id='llm-response', 
                    style={'border': '1px solid #ddd',
                           'borderRadius': '8px',
                           'backgroundColor': '#f8f9fa',
                           'maxHeight': '33%',
                           'overflowY': 'scroll'})
                    
                ], style={
                    'width': '38%', 'display': 'inline-grid', 'verticalAlign': 'top',})
                
            ], style={'maxWidth': '1400px',"display":"inline"})
            
        ], style={'padding': '20px', 'backgroundColor': '#f5f5f5', 'minHeight': '100vh'})
        
        # Callbacks for charts
        @self.app.callback(
            [Output('metric-trend', 'figure'),
             Output('profitability-analysis', 'figure')],
            [Input('company-selector', 'value'),
             Input('metric-selector', 'value')]
        )
        def update_charts(selected_companies, selected_metric):
            metric_trend_fig = create_metric_trend_chart(self.df,selected_metric, selected_companies)
            profitability_fig = create_profitability_comparison(self.df,selected_companies)
            return metric_trend_fig, profitability_fig
        
        # Callback for LLM queries
        @self.app.callback(
            Output('llm-response', 'children'),
            [Input('submit-query', 'n_clicks')] + 
            [Input(f'sample-q-{i}', 'n_clicks') for i in range(3)],
            [State('user-query', 'value')] + 
            [State(f'sample-q-{i}', 'children') for i in range(3)],
            prevent_initial_call=True
        )
        def process_query(submit_clicks, *args):
            ctx = dash.callback_context
            
            if not ctx.triggered:
                return dash.no_update
            
            # Separate clicks from states
            sample_clicks = args[:3]  
            user_query_value = args[3]  
            sample_questions_text = args[4:7] 
            
            # Determine which button was clicked
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            query = None
            
            if button_id == 'submit-query':
                query = user_query_value
            elif button_id.startswith('sample-q-'):
                sample_idx = int(button_id.split('-')[-1])
                query = sample_questions_text[sample_idx]
            
            if not query or (isinstance(query, str) and not query.strip()):
                return html.Div("Please enter a question or click a sample question.", 
                              style={'color': '#dc3545'})
            
            # Ensure query is a string
            if not isinstance(query, str):
                return html.Div("Invalid query format.", style={'color': '#dc3545'})
            
            # Process the query
            try:
                response_text = self.query_financial_data(query.strip())
                
                return html.Div([
                    html.H4(f"📝 Query: {query}", style={'color': '#495057', 'borderBottom': '2px solid #dee2e6', 'paddingBottom': '10px'}),
                    html.Div([
                        dcc.Markdown(response_text, style={'lineHeight': '1.6'})
                    ], style={'marginTop': '15px'}),
                    html.Hr(),
                    html.P(f"⏰ Generated at {datetime.now().strftime('%H:%M:%S')}", 
                          style={'fontSize': '12px', 'color': '#6c757d', 'textAlign': 'right'})
                ])
                
            except Exception as e:
                return html.Div([
                    html.H4("❌ Error Processing Query", style={'color': '#dc3545'}),
                    html.P(f"Sorry, there was an error: {str(e)}")
                ])
        
        # Callback to update textarea when sample question is clicked
        @self.app.callback(
            Output('user-query', 'value'),
            [Input(f'sample-q-{i}', 'n_clicks') for i in range(3)],
            [State(f'sample-q-{i}', 'children') for i in range(3)],
            prevent_initial_call=True
        )
        def update_textarea(*args):
            ctx = dash.callback_context
            
            if not ctx.triggered:
                return dash.no_update
                
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            if button_id.startswith('sample-q-'):
                sample_idx = int(button_id.split('-')[-1])
                sample_clicks = args[:3]  # First 3 are clicks
                sample_texts = args[3:6]  # Next 3 are the text contents
                return sample_texts[sample_idx]  # Return the sample question text
                
            return dash.no_update

    def run_dashboard(self, debug=True, port=8050):
        """Run the integrated dashboard application"""
        if not self.load_and_process_data():
            print("Failed to load data. Please check the data path.")
            return
            
        self.setup_dash_app()
        
        print(f"🚀 Starting integrated dashboard with AI assistant on http://localhost:{port}")
        print("Features available:")
        print("  📊 Interactive financial charts")
        print("  🤖 AI-powered query system") 
        print("  💬 Natural language financial analysis")
        print("  🎯 Context-aware responses")
        
        self.app.run(debug=debug, port=port)

# Standalone query system class for command-line usage
class StandaloneQuerySystem:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = os.path.join(os.getcwd(), 'data', 'processed', 'financial_data.csv')
        
        self.dashboard = IntegratedFinancialDashboard(data_path)
        
    def run_cli_session(self):
        """Run command-line interactive session"""
        if not self.dashboard.load_and_process_data():
            print("❌ Failed to load financial data. Exiting.")
            return
        
        print("🤖 FINANCIAL AI ASSISTANT - CLI MODE")
        print("="*60)
        print("Ask me anything about REXP and DIPD financial data!")
        print("Type 'quit' to exit, 'help' for examples.")
        print("="*60)
        
        # Sample questions
        sample_questions = [
            "What is the revenue trend for REXP over the last 4 quarters?",
            "Compare the profitability margins between REXP and DIPD",
            "Which company has better financial performance and why?",
            "What was the highest revenue quarter for each company?",
            "Calculate the revenue growth rate for DIPD year-over-year",
            "Show me the operating margin trends for both companies",
            "What are the key financial risks I should be aware of?",
            "Which company is more financially stable?",
            "Analyze the cost structure differences between REXP and DIPD",
            "What seasonal patterns do you see in the revenue data?"
        ]
        
        while True:
            try:
                user_input = input("\n🔍 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using Financial AI Assistant!")
                    break
                    
                elif user_input.lower() in ['help', 'examples']:
                    print("\n📋 EXAMPLE QUERIES:")
                    print("="*60)
                    for i, example in enumerate(sample_questions, 1):
                        print(f"{i:2d}. {example}")
                    print("="*60)
                    continue
                
                elif not user_input:
                    continue
                
                print("\n🔄 Processing your query...")
                
                # Process query
                response = self.dashboard.query_financial_data(user_input)
                
                print(f"\n🤖 AI RESPONSE:")
                print("="*60)
                print(response)
                print("="*60)
                print(f"⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Session ended by user.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

# Usage examples and main execution
def main():
    """Main function with usage options"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--cli':
            # Run CLI mode
            cli_system = StandaloneQuerySystem()
            cli_system.run_cli_session()
        elif sys.argv[1] == '--web':
            # Run web dashboard
            dashboard = IntegratedFinancialDashboard()
            dashboard.run_dashboard()
        else:
            print("Usage:")
            print("  python script.py --web    # Run web dashboard")
            print("  python script.py --cli    # Run CLI assistant")
    else:
        # Default: run web dashboard
        print("🌐 Starting web dashboard by default...")
        print("Use --cli flag for command-line mode")
        dashboard = IntegratedFinancialDashboard()
        dashboard.run_dashboard()

if __name__ == '__main__':
    main()