#!/bin/bash

set -e

LOG_ROOT="./result_logs"

# Function to sanitize directory name for path (e.g., remove subfolders)
sanitize_dir() {
  echo "$1" | cut -d'/' -f1
}

# Function to run the build and capture last 20 lines of output
run_build() {
  local file_path=$1
  shift
  local specs=("$@")
  local dir=$(sanitize_dir "$file_path")

  for spec in "${specs[@]}"; do
    echo "🔧 Building $file_path with spec '$spec'..."

    log_dir="$LOG_ROOT/$dir"
    mkdir -p "$log_dir"
    log_file="$log_dir/$spec.log"

    # Run and capture all output temporarily
    tmp_output=$(mktemp)
    rm -rf build
    if go run "$file_path" -o build -w "$spec" -quiet &> "$tmp_output"; then
      echo "✅ Build succeeded for $file_path [$spec]"
    else
      echo "❌ Build failed for $file_path [$spec]"
    fi

    # Save only the last 20 lines to the log
    tail -n 20 "$tmp_output" > "$log_file"
    rm "$tmp_output"
  done
}

# Run builds
run_build dsb_hotel/wiring/main.go original
run_build dsb_sn/wiring/main.go docker
run_build leaf/wiring/main.go docker thrift http timeout_demo timeout_retries_demo xtrace_logger ot_logger govector
run_build sockshop/wiring/main.go basic grpc docker rabbit
run_build train_ticket/wiring/main.go docker

echo "📁 Logs saved under $LOG_ROOT/"
echo "✅ All builds completed."
