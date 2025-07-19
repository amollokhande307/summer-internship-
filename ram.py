import psutil
import time
from datetime import datetime

def get_memory_info():
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024**3)
    used_gb = memory.used / (1024**3)
    available_gb = memory.available / (1024**3)
    return {
        'total': total_gb,
        'used': used_gb,
        'available': available_gb,
        'percentage': memory.percent
    }

def format_memory_display(memory_info):
    return f"""
📊 *System Memory Information*

🔹 *Total RAM:* {memory_info['total']:.2f} GB
🔹 *Used Memory:* {memory_info['used']:.2f} GB  
🔹 *Available Memory:* {memory_info['available']:.2f} GB
🔹 *Usage Percentage:* {memory_info['percentage']:.1f}%

⏰ *Last Updated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

def is_streamlit():
    try:
        import streamlit as st
        _ = st.session_state
        return True
    except ImportError:
        return False
    except AttributeError:
        return False

def streamlit_app():
    import streamlit as st
    import pandas as pd
    
    st.set_page_config(
        page_title="System RAM Monitor",
        page_icon="💾",
        layout="wide"
    )
    
    st.title("💾 System RAM Memory Monitor")
    st.markdown("Real-time system memory information display")
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        memory_info = get_memory_info()
        st.markdown(format_memory_display(memory_info))
        st.progress(memory_info['percentage'] / 100)
        st.subheader("📈 Memory Breakdown")
        chart_data = pd.DataFrame({
            'Size (GB)': [memory_info['used'], memory_info['available']]
        }, index=['Used', 'Available'])
        st.bar_chart(chart_data)
    
    with col2:
        st.subheader("⚙ Controls")
        auto_refresh = st.checkbox("Auto Refresh (5s)", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
        if st.button("🔄 Refresh Now"):
            st.rerun()
        if memory_info['percentage'] < 50:
            st.success("✅ Memory usage is healthy")
        elif memory_info['percentage'] < 80:
            st.warning("⚠ Memory usage is moderate")
        else:
            st.error("🚨 Memory usage is high")
        st.info(f"Free: {memory_info['available']:.1f} GB")
    
    st.subheader("🖥 Additional System Info")
    try:
        cpu_count = psutil.cpu_count(logical=True)
        cpu_physical = psutil.cpu_count(logical=False)
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime_days = (datetime.now() - boot_time).days
    except Exception as e:
        st.error(f"Error getting system info: {e}")
        cpu_count = cpu_physical = uptime_days = "N/A"
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("CPU Cores (Logical)", cpu_count)
    with col4:
        st.metric("CPU Cores (Physical)", cpu_physical)
    with col5:
        st.metric("System Uptime", f"{uptime_days} days")
    
    if auto_refresh:
        placeholder = st.empty()
        for i in range(5, 0, -1):
            placeholder.text(f"Refreshing in {i} seconds...")
            time.sleep(1)
        placeholder.empty()
        st.rerun()

def console_app():
    print("=" * 50)
    print("💾 SYSTEM MEMORY INFORMATION")
    print("=" * 50)
    try:
        memory_info = get_memory_info()
        print(f"🔹 Total RAM:        {memory_info['total']:.2f} GB")
        print(f"🔹 Used Memory:      {memory_info['used']:.2f} GB")
        print(f"🔹 Available Memory: {memory_info['available']:.2f} GB")
        print(f"🔹 Usage Percentage: {memory_info['percentage']:.1f}%")
        print(f"⏰ Timestamp:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if memory_info['percentage'] < 50:
            print("✅ Status: Memory usage is healthy")
        elif memory_info['percentage'] < 80:
            print("⚠ Status: Memory usage is moderate")
        else:
            print("🚨 Status: Memory usage is high")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Error getting memory info: {e}")

def main():
    if is_streamlit():
        streamlit_app()
    else:
        console_app()
        try:
            response = input("\nStart continuous monitoring? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                print("Starting continuous monitoring... Press Ctrl+C to stop.\n")
                while True:
                    time.sleep(5)
                    print("\n" + "🔄 Refreshing..." + "\n")
                    console_app()
        except KeyboardInterrupt:
            print("\n👋 Memory monitor stopped.")
        except Exception:
            print("\nSingle run completed.")

if __name__ == "__main__":
    main()