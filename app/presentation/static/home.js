const $ = (id) => document.getElementById(id);
let lastResults = [];

const IGNORED_PATTERNS = [
  "venv", ".venv", "env", ".env",
  "site-packages", "dist-packages",
  "__pycache__", ".git", "node_modules"
];

function shouldIgnoreFile(file) {
  // Lấy đường dẫn tương đối (nếu chọn thư mục) hoặc tên file
  const pathStr = (file.webkitRelativePath || file.name || "").replace(/\\/g, "/");
  const parts = pathStr.split("/");
  return parts.some(part => IGNORED_PATTERNS.includes(part));
}

$("btn-scan").addEventListener("click", async () => {
  const rawFiles = $("files").files;
  if (!rawFiles.length) { $("status").textContent = "Chưa chọn file."; return; }

  // Lọc bỏ các file thuộc môi trường ảo hoặc thư viện thứ ba
  const files = Array.from(rawFiles).filter(f => !shouldIgnoreFile(f));
  if (!files.length) { 
    $("status").textContent = "Tất cả các file đã chọn đều thuộc danh sách bị bỏ qua."; 
    return; 
  }

  const form = new FormData();
  for (const f of files) form.append("files", f);

  $("status").textContent = `Đang quét ${files.length} file (đã lọc)...`;
  $("result").textContent = "";
  $("export").hidden = true;

  try {
    const res = await fetch("/api/scan", { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || res.statusText);

    lastResults = data.results;
    $("result").textContent = data.results
      .map((r) => `=== Nhóm ${r.chunk} (${r.files.length} file) ===\n${r.files.join(", ")}\n\n${r.report}`)
      .join("\n\n");
    $("status").textContent = `Xong: ${data.total_files} file, ${data.results.length} nhóm.`;
    $("export").hidden = false;
  } catch (e) {
    $("status").textContent = "Lỗi: " + e.message;
  }
});

document.querySelectorAll("#export button").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ format: btn.dataset.fmt, results: lastResults }),
    });
    if (!res.ok) { $("status").textContent = "Xuất file thất bại."; return; }
    const blob = await res.blob();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `decanote_report.${btn.dataset.fmt}`;
    a.click();
    URL.revokeObjectURL(a.href);
  });
});