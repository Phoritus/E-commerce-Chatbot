HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Estate API</title>
    <!-- 1. โหลด Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 2. ตั้งค่าฟอนต์ที่สวยงาม (Inter) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">

    <!-- 3. การ์ดต้อนรับตรงกลาง -->
    <div class="bg-white p-10 md:p-12 rounded-xl shadow-2xl text-center max-w-lg mx-4">
        
        <!-- ไอคอนบ้าน (SVG) -->
        <svg 
        class="w-20 h-20 text-blue-600 mx-auto" 
        xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 24 24" 
        fill="currentColor"
      >
          <path d="M17 4H7v2H5v2H3v12h4v-2h10v2h4V8h-2V6h-2zm0 2v2h2v2H5V8h2V6zm2 10H5v-4h14zm-2-3h-2v2h2zM7 13h2v2H7z" />
      </svg>

        <!-- หัวเรื่อง -->
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mt-6">
            Welcome to Chat Bot API
        </h1>
        
        <!-- คำอธิบาย -->
        <p class="text-gray-600 mt-3 text-lg">
            A modern API for managing and use chat bot services.
        </p>
        
        <!-- 4. ปุ่มที่สำคัญที่สุด: ลิงก์ไปยัง /docs -->
        <a href="/docs" 
           class="mt-8 inline-block px-8 py-3 bg-blue-600 text-white text-lg font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition-colors duration-300">
            View API Documentation
        </a>
    </div>

</body>
</html>
"""