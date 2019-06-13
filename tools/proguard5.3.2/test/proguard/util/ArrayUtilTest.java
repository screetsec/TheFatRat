package proguard.util;

import org.junit.Assert;
import org.junit.Test;

public class ArrayUtilTest {

	@Test
	public void testEqualByte() {
		Assert.assertFalse(ArrayUtil.equal(new byte[]{3, 2, 1},
			new byte[]{1, 2, 3}, 4)
		);

		Assert.assertTrue(ArrayUtil.equal(new byte[]{1, 2, 3},
			new byte[]{1, 2, 3}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal(new byte[]{1, 2, 3},
			new byte[]{1, 2, 3, 4}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal((byte[]) null,
			null, 0)
		);
	}

	@Test
	public void testEqualShort() {
		Assert.assertFalse(ArrayUtil.equal(new short[]{3, 2, 1},
			new short[]{1, 2, 3}, 4)
		);

		Assert.assertTrue(ArrayUtil.equal(new short[]{1, 2, 3},
			new short[]{1, 2, 3}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal(new short[]{1, 2, 3},
			new short[]{1, 2, 3, 4}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal((short[]) null,
			null, 0)
		);
	}

	@Test
	public void testEqualInt() {
		Assert.assertFalse(ArrayUtil.equal(new int[]{3, 2, 1},
			new int[]{1, 2, 3}, 4)
		);

		Assert.assertTrue(ArrayUtil.equal(new int[]{1, 2, 3},
			new int[]{1, 2, 3}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal(new int[]{1, 2, 3},
			new int[]{1, 2, 3, 4}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal((int[]) null,
			null, 0)
		);
	}

	@Test
	public void testEqualObject() {
		Assert.assertFalse(ArrayUtil.equal(new Object[]{3, 2, 1},
			new Object[]{1, 2, 3}, 4)
		);

		Assert.assertTrue(ArrayUtil.equal(new Object[]{1, 2, 3},
			new Object[]{1, 2, 3}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal(new Object[]{1, 2, 3},
			new Object[]{1, 2, 3, 4}, 3)
		);
		Assert.assertTrue(ArrayUtil.equal((Object[]) null,
			null, 0)
		);
	}

	@Test
	public void testEqualOrNull() {
		Assert.assertTrue(ArrayUtil.equalOrNull(null, null));
		Assert.assertTrue(ArrayUtil.equalOrNull(new Object[]{1, 2, 3},
			new Object[]{1, 2, 3, 4})
		);

		Assert.assertFalse(ArrayUtil.equalOrNull(null, new Object[]{null, 0}));
		Assert.assertFalse(ArrayUtil.equalOrNull(new Object[]{3, 2, 1},
			new Object[]{1, 2, 3, 4})
		);
	}

	@Test
	public void testEqualOrNullSize() {
		Assert.assertTrue(ArrayUtil.equalOrNull(null, null, 1));
		Assert.assertTrue(ArrayUtil.equalOrNull(new Object[]{1, 2, 3},
			new Object[]{1, 2, 3, 4}, 3)
		);

		Assert.assertFalse(ArrayUtil.equalOrNull(null,
			new Object[]{null, 0}, 1)
		);
		Assert.assertFalse(ArrayUtil.equalOrNull(new Object[]{3, 2, 1},
			new Object[]{1, 2, 3, 4}, 3)
		);
	}

	@Test
	public void testHashCodeByte() {
		Assert.assertEquals(0,
			ArrayUtil.hashCode(new byte[0], 0)
		);
		Assert.assertEquals(4,
			ArrayUtil.hashCode(new byte[]{7, 0, 3}, 3)
		);
	}

	@Test
	public void testHashCodeShort() {
		Assert.assertEquals(0,
			ArrayUtil.hashCode(new short[0], 0)
		);
		Assert.assertEquals(4,
			ArrayUtil.hashCode(new short[]{7, 0, 3}, 3)
		);
	}

	@Test
	public void testHashCodeInt() {
		Assert.assertEquals(0,
			ArrayUtil.hashCode(new int[0], 0)
		);
		Assert.assertEquals(4,
			ArrayUtil.hashCode(new int[]{7, 0, 3}, 3)
		);
	}

	@Test
	public void testHashCodeObject() {
		Assert.assertEquals(0,
			ArrayUtil.hashCode(new Object[0], 0)
		);
		Assert.assertEquals(4,
			ArrayUtil.hashCode(new Object[]{7, 0, 3}, 3)
		);
	}

	@Test
	public void testHashCodeOrNull() {
		Assert.assertEquals(4,
			ArrayUtil.hashCodeOrNull(new Object[]{7, 0, 3})
		);
		Assert.assertEquals(0,
			ArrayUtil.hashCodeOrNull(null)
		);
	}

	@Test
	public void testHashCodeOrNullSize() {
		Assert.assertEquals(4,
			ArrayUtil.hashCodeOrNull(new Object[]{7, 0, 3}, 3)
		);
		Assert.assertEquals(0,
			ArrayUtil.hashCodeOrNull(null, 0)
		);
	}

	@Test
	public void testCompareByte() {
		Assert.assertEquals(-1, ArrayUtil.compare(
			new byte[]{1, 2}, 2,
			new byte[]{1, 2, 3, 0, 0}, 5)
		);
		Assert.assertEquals(-1, ArrayUtil.compare(
			new byte[]{0, 1, 2}, 3,
			new byte[]{2, 1, 0}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new byte[0], 0,
			new byte[0], 0)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new byte[]{0, 1, 2}, 3,
			new byte[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new byte[]{0, 1, 2}, 3,
			new byte[]{0, 1, 2, 3, 4}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new byte[]{0, 1, 2, 3, 4}, 3,
			new byte[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(1, ArrayUtil.compare(
			new byte[]{2, 1, 0}, 3,
			new byte[]{0, 1, 2}, 3)
		);

	}

	@Test
	public void testCompareShort() {
		Assert.assertEquals(-1, ArrayUtil.compare(
			new short[]{1, 2}, 2,
			new short[]{1, 2, 3, 0, 0}, 5)
		);
		Assert.assertEquals(-1, ArrayUtil.compare(
			new short[]{0, 1, 2}, 3,
			new short[]{2, 1, 0}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new short[0], 0,
			new short[0], 0)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new short[]{0, 1, 2}, 3,
			new short[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new short[]{0, 1, 2}, 3,
			new short[]{0, 1, 2, 3, 4}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new short[]{0, 1, 2, 3, 4}, 3,
			new short[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(1, ArrayUtil.compare(
			new short[]{2, 1, 0}, 3,
			new short[]{0, 1, 2}, 3)
		);
	}

	@Test
	public void testCompareInt() {
		Assert.assertEquals(-1, ArrayUtil.compare(
			new int[]{1, 2}, 2,
			new int[]{1, 2, 3, 0, 0}, 5)
		);
		Assert.assertEquals(-1, ArrayUtil.compare(
			new int[]{0, 1, 2}, 3,
			new int[]{2, 1, 0}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new int[0], 0,
			new int[0], 0)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new int[]{0, 1, 2}, 3,
			new int[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new int[]{0, 1, 2}, 3,
			new int[]{0, 1, 2, 3, 4}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new int[]{0, 1, 2, 3, 4}, 3,
			new int[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(1, ArrayUtil.compare(
			new int[]{2, 1, 0}, 3,
			new int[]{0, 1, 2}, 3)
		);
	}

	@Test
	public void testCompareComparable() {
		Assert.assertEquals(-1, ArrayUtil.compare(
			new Comparable[]{1, 2}, 2,
			new Comparable[]{1, 2, 3, 0, 0}, 5)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new Comparable[0], 0,
			new Comparable[0], 0)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new Comparable[]{0, 1, 2}, 3,
			new Comparable[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new Comparable[]{0, 1, 2}, 3,
			new Comparable[]{0, 1, 2, 3, 4}, 3)
		);
		Assert.assertEquals(0, ArrayUtil.compare(
			new Comparable[]{0, 1, 2, 3, 4}, 3,
			new Comparable[]{0, 1, 2}, 3)
		);
		Assert.assertEquals(1, ArrayUtil.compare(
			new Comparable[]{2, 1, 0}, 3,
			new Comparable[]{0, 1, 2}, 3)
		);
	}

	@Test
	public void testExtendArrayBoolean() {
		Assert.assertArrayEquals(new boolean[0],
			ArrayUtil.extendArray(new boolean[0], 0)
		);
		Assert.assertArrayEquals(new boolean[]{true, true, true, false, false},
			ArrayUtil.extendArray(new boolean[]{true, true, true}, 5)
		);
	}

	@Test
	public void testEnsureArraySizeBoolean() {
		boolean[] booleans = new boolean[]{false, false, true};

		Assert.assertArrayEquals(new boolean[]{true, true, true, true},
			ArrayUtil.ensureArraySize(booleans, 4, true)
		);

		booleans = new boolean[]{false, false, true, true};

		Assert.assertArrayEquals(new boolean[]{false, false, false, true},
			ArrayUtil.ensureArraySize(booleans, 3, false)
		);
		Assert.assertArrayEquals(new boolean[]{false, false, false, false},
			ArrayUtil.ensureArraySize(booleans, 4, false)
		);
	}

	@Test
	public void testAddByte() {
		Assert.assertArrayEquals(new byte[]{0, 0, 0},
			ArrayUtil.add(new byte[]{1, 0, 0}, 0, (byte) 0)
		);
		Assert.assertArrayEquals(new byte[]{1, 0, 0},
			ArrayUtil.add(new byte[]{1, 0, 0}, 1, (byte) 0)
		);
		Assert.assertArrayEquals(new byte[]{1, 2, 3, 0},
			ArrayUtil.add(new byte[]{1, 2, 3}, 3, (byte) 0)
		);
	}

	@Test
	public void testInsertByte() {
		Assert.assertArrayEquals(new byte[]{1, 2, 3},
			ArrayUtil.insert(new byte[]{1, 2}, 2, 2, (byte) 3)
		);
		Assert.assertArrayEquals(new byte[]{1, 2, 2, 3},
			ArrayUtil.insert(new byte[]{1, 2, 3}, 3, 2, (byte) 2)
		);
	}

	@Test
	public void testRemoveByte() {
		byte[] bytes = new byte[]{1, 2, 3, 4};

		ArrayUtil.remove(bytes, 4, 1);

		Assert.assertArrayEquals(new byte[]{1, 3, 4, 0}, bytes);

		bytes = new byte[]{1, 2, 3, 4};

		ArrayUtil.remove(bytes, 4, 2);
		ArrayUtil.remove(bytes, 3, 1);

		Assert.assertArrayEquals(new byte[]{1, 4, 0, 0}, bytes);
	}

	@Test
	public void testExtendArrayByte() {
		Assert.assertArrayEquals(new byte[0],
			ArrayUtil.extendArray(new byte[0], 0)
		);
		Assert.assertArrayEquals(new byte[]{1, 2, 3, 0, 0},
			ArrayUtil.extendArray(new byte[]{1, 2, 3}, 5)
		);
	}

	@Test
	public void testEnsureArraySizeByte() {
		Assert.assertArrayEquals(new byte[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new byte[]{1, 2, 3}, 4, (byte) 2)
		);
		Assert.assertArrayEquals(new byte[]{2, 2, 2, 4},
			ArrayUtil.ensureArraySize(new byte[]{1, 2, 3, 4}, 3, (byte) 2)
		);
		Assert.assertArrayEquals(new byte[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new byte[]{1, 2, 3, 4}, 4, (byte) 2)
		);
	}

	@Test
	public void testAddShort() {
		Assert.assertArrayEquals(new short[]{0, 0, 0},
			ArrayUtil.add(new short[]{1, 0, 0}, 0, (short) 0)
		);
		Assert.assertArrayEquals(new short[]{1, 0, 0},
			ArrayUtil.add(new short[]{1, 0, 0}, 1, (short) 0)
		);
		Assert.assertArrayEquals(new short[]{1, 0, 0, 0},
			ArrayUtil.add(new short[]{1, 0, 0}, 3, (short) 0)
		);
	}

	@Test
	public void testInsertShort() {
		Assert.assertArrayEquals(new short[]{1, 2, 3},
			ArrayUtil.insert(new short[]{1, 2}, 2, 2, (short) 3)
		);
		Assert.assertArrayEquals(new short[]{1, 2, 2, 3},
			ArrayUtil.insert(new short[]{1, 2, 3}, 3, 2, (short) 2)
		);
	}

	@Test
	public void testRemoveShort() {
		short[] shorts = new short[]{1, 2, 3, 4};

		ArrayUtil.remove(shorts, 4, 1);

		Assert.assertArrayEquals(new short[]{1, 3, 4, 0}, shorts);

		shorts = new short[]{1, 2, 3, 4};

		ArrayUtil.remove(shorts, 4, 2);
		ArrayUtil.remove(shorts, 3, 1);

		Assert.assertArrayEquals(new short[]{1, 4, 0, 0}, shorts);
	}

	@Test
	public void testExtendArrayShort() {
		Assert.assertArrayEquals(new short[0],
			ArrayUtil.extendArray(new short[0], 0)
		);
		Assert.assertArrayEquals(new short[]{1, 2, 3, 0, 0},
			ArrayUtil.extendArray(new short[]{1, 2, 3}, 5)
		);
	}

	@Test
	public void testEnsureArraySizeShort() {
		Assert.assertArrayEquals(new short[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new short[]{1, 2, 3}, 4, (short) 2)
		);
		Assert.assertArrayEquals(new short[]{2, 2, 2, 4},
			ArrayUtil.ensureArraySize(new short[]{1, 2, 3, 4}, 3, (short) 2)
		);
		Assert.assertArrayEquals(new short[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new short[]{1, 2, 3, 4}, 4, (short) 2)
		);
	}

	@Test
	public void testAddInt() {
		Assert.assertArrayEquals(new int[]{0, 0, 0},
			ArrayUtil.add(new int[]{1, 0, 0}, 0, 0)
		);
		Assert.assertArrayEquals(new int[]{1, 0, 0},
			ArrayUtil.add(new int[]{1, 0, 0}, 1, 0)
		);
		Assert.assertArrayEquals(new int[]{1, 0, 0, 0},
			ArrayUtil.add(new int[]{1, 0, 0}, 3, 0)
		);
	}

	@Test
	public void testInsertInt() {
		Assert.assertArrayEquals(new int[]{1, 2, 3},
			ArrayUtil.insert(new int[]{1, 2}, 2, 2, 3)
		);
		Assert.assertArrayEquals(new int[]{1, 2, 2, 3},
			ArrayUtil.insert(new int[]{1, 2, 3}, 3, 2, 2)
		);
	}

	@Test
	public void testRemoveInt() {
		int[] ints = new int[]{1, 2, 3, 4};

		ArrayUtil.remove(ints, 4, 1);

		Assert.assertArrayEquals(new int[]{1, 3, 4, 0}, ints);

		ints = new int[]{1, 2, 3, 4};

		ArrayUtil.remove(ints, 4, 2);
		ArrayUtil.remove(ints, 3, 1);

		Assert.assertArrayEquals(new int[]{1, 4, 0, 0}, ints);
	}

	@Test
	public void testExtendArrayInt() {
		Assert.assertArrayEquals(new int[0],
			ArrayUtil.extendArray(new int[0], 0))
		;
		Assert.assertArrayEquals(new int[]{1, 2, 3, 0, 0},
			ArrayUtil.extendArray(new int[]{1, 2, 3}, 5)
		);
	}

	@Test
	public void testEnsureArraySizeInt() {
		Assert.assertArrayEquals(new int[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new int[]{1, 2, 3}, 4, 2)
		);
		Assert.assertArrayEquals(new int[]{2, 2, 2, 4},
			ArrayUtil.ensureArraySize(new int[]{1, 2, 3, 4}, 3, 2)
		);
		Assert.assertArrayEquals(new int[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new int[]{1, 2, 3, 4}, 4, 2)
		);
	}

	@Test
	public void testAddLong() {
		Assert.assertArrayEquals(new long[]{0, 0, 0},
			ArrayUtil.add(new long[]{1, 0, 0}, 0, 0)
		);
		Assert.assertArrayEquals(new long[]{1, 0, 0},
			ArrayUtil.add(new long[]{1, 0, 0}, 1, 0)
		);
		Assert.assertArrayEquals(new long[]{1, 0, 0, 0},
			ArrayUtil.add(new long[]{1, 0, 0}, 3, 0)
		);
	}

	@Test
	public void testInsertLong() {
		Assert.assertArrayEquals(new long[]{1, 2, 3},
			ArrayUtil.insert(new long[]{1, 2}, 2, 2, 3)
		);
		Assert.assertArrayEquals(new long[]{1, 2, 2, 3},
			ArrayUtil.insert(new long[]{1, 2, 3}, 3, 2, 2)
		);
	}

	@Test
	public void testRemoveLong() {
		long[] longs = new long[]{1, 2, 3, 4};

		ArrayUtil.remove(longs, 4, 1);

		Assert.assertArrayEquals(new long[]{1, 3, 4, 0}, longs);

		longs = new long[]{1, 2, 3, 4};

		ArrayUtil.remove(longs, 4, 2);
		ArrayUtil.remove(longs, 3, 1);

		Assert.assertArrayEquals(new long[]{1, 4, 0, 0}, longs);
	}

	@Test
	public void testExtendArrayLong() {
		Assert.assertArrayEquals(new long[0],
			ArrayUtil.extendArray(new long[0], 0)
		);
		Assert.assertArrayEquals(new long[]{1, 2, 3, 0, 0},
			ArrayUtil.extendArray(new long[]{1, 2, 3}, 5)
		);
	}

	@Test
	public void testEnsureArraySizeLong() {
		Assert.assertArrayEquals(new long[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new long[]{1, 2, 3}, 4, 2)
		);
		Assert.assertArrayEquals(new long[]{2, 2, 2, 4},
			ArrayUtil.ensureArraySize(new long[]{1, 2, 3, 4}, 3, 2)
		);
		Assert.assertArrayEquals(new long[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new long[]{1, 2, 3, 4}, 4, 2)
		);
	}

	@Test
	public void testAddObject() {
		Assert.assertArrayEquals(new Object[]{0, 0, 0},
			ArrayUtil.add(new Object[]{1, 0, 0}, 0, 0)
		);
		Assert.assertArrayEquals(new Object[]{1, 0, 0},
			ArrayUtil.add(new Object[]{1, 0, 0}, 1, 0)
		);
		Assert.assertArrayEquals(new Object[]{1, 2, 3, 0},
			ArrayUtil.add(new Object[]{1, 2, 3}, 3, 0)
		);
	}

	@Test
	public void testInsertObject() {
		Assert.assertArrayEquals(new Object[]{1, 2, 3},
			ArrayUtil.insert(new Object[]{1, 2}, 2, 2, 3)
		);
		Assert.assertArrayEquals(new Object[]{1, 2, 2, 3},
			ArrayUtil.insert(new Object[]{1, 2, 3}, 3, 2, 2)
		);
	}

	@Test
	public void testRemoveObject() {
		Object[] objects = new Object[]{1, 2, 3, 4};

		ArrayUtil.remove(objects, 4, 1);

		Assert.assertArrayEquals(new Object[]{1, 3, 4, null}, objects);

		objects = new Object[]{1, 2, 3, 4};

		ArrayUtil.remove(objects, 4, 2);
		ArrayUtil.remove(objects, 3, 1);

		Assert.assertArrayEquals(new Object[]{1, 4, null, null}, objects);
	}

	@Test
	public void testExtendArrayObject() {
		Assert.assertArrayEquals(new Object[]{null},
			ArrayUtil.extendArray(new Object[]{null}, 0)
		);
		Assert.assertArrayEquals(new Object[]{1, 2, 3, null, null},
			ArrayUtil.extendArray(new Object[]{1, 2, 3}, 5)
		);
	}

	@Test
	public void testEnsureArraySizeObject() {
		Assert.assertArrayEquals(new Object[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new Object[]{1, 2, 3}, 4, 2)
		);
		Assert.assertArrayEquals(new Object[]{2, 2, 2, 4},
			ArrayUtil.ensureArraySize(new Object[]{1, 2, 3, 4}, 3, 2)
		);
		Assert.assertArrayEquals(new Object[]{2, 2, 2, 2},
			ArrayUtil.ensureArraySize(new Object[]{1, 2, 3, 4}, 4, 2)
		);
	}
}
